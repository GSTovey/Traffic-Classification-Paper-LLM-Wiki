# Non-uniformity is All You Need: Eficient and Timely Encrypted Trafic Classification With ECHO

Shilo Daum The Hebrew University Jerusalem, Israel shilo.daum@mail.huji.ac.il

Anat Bremler-Barr Tel Aviv University Tel Aviv, Israel anatbr@tauex.tau.ac.il

Tal Shapira The Hebrew University Jerusalem, Israel talshapirala@gmail.com

David Hay\* The Hebrew University Jerusalem, Israel dhay@cs.huji.ac.il

## ABSTRACT

With 95% of Internet traffic now encrypted, an effective approach to classifying this traffic is crucial for network security and management. This paper introduces ECHO—a novel optimization process for ML/DL-based encrypted traffic classification. ECHO targets both classification time and memory utilization and incorporates two innovative techniques.

The first component, HO (Hyperparameter Optimization of binnings), aims at creating efficient traffic representations. While previous research often uses representations that map packet sizes and packet arrival times to fixed-sized bins, we show that non-uniform binnings are significantly more efficient. These non-uniform binnings are derived by employing a hyperparameter optimization algorithm in the training stage. HO significantly improves accuracy given a required representation size, or, equivalently, achieves comparable accuracy using smaller representations.

Then, we introduce EC (Early Classification of traffic), which enables faster classification using a cascade of classifiers adapted for different exit times, where classification is based on the level of confidence. EC reduces the average classification latency by up to 90%. Remarkably, this method not only maintains classification accuracy but also, in certain cases, improves it.

Using three publicly available datasets, we demonstrate that the combined method, Early Classification with Hyperparameter Optimization (ECHO), leads to a significant improvement in classification efficiency.

## 1 INTRODUCTION

Internet traffic classification is a critical challenge in network management, security, and optimization. Traffic classification can be used for application identification [48], traffic categorization [3, 16], identifying encryption methods like VPN or Tor [32], detecting malicious activities such as Distributed Denial of Service (DDoS) attacks [13, 49, 52], and device fingerprinting [17].

In the past, classification methods such as port-based classification (using the predefined ports associated with specific services or applications) or signature-based Deep Packet Inspection (DPI) were considered sufficient (cf. [2, 22]).

However, the use of random ports, shared port usage between applications, and most importantly, the widespread adoption of encryption protocols—such as TLS/SSL encryption, VPN tunneling, and anonymous communication technologies (e.g. Tor [18, 39])—have significantly hindered the ability to inspect and classify traffic based on these approaches.

Thus, new approaches were introduced to deal with encrypted traffic, mostly focused on extracting features from each flow (namely, the flow representation) and applying Machine Learning (ML) or Deep Learning (DL) methods to classify it. As most data is obfuscated, these methods typically use as input only the size of packets, their inter-arrival times, and their direction.

While many proposed methods claim high accuracy in classification, implementing these approaches in reallife scenarios can be challenging due to the large volume of traffic (namely, hundreds of Gb/s in large ISPs) and the huge number of concurrent connections (namely, millions of new connection per second<sup>1</sup>). Thus, storing flow content, headers, or representations requires considerable memory resources. Moreover, the deployment of DL or large ML models demands significant computational power.

To reduce both memory and compute, flow representations often aggregate values, and each packet size (or arrival time) is mapped to a bin. The representation then typically holds a counter for each bin, tracking the number of packets whose size (or arrival time) falls within that bin. This is most commonly done in a uniform manner with all bins being the same size. However, such coarse-grained uniform binning might fail to capture subtle nuances in traffic patterns.

This paper first explores non-uniform binnings, as realworld traffic data often exhibit non-uniform patterns. We introduce variable-sized bins, each representing an interval of values, allowing for a more fine-grained and adaptive approach to capturing non-uniform traffic patterns, with smaller representations. Examples of uniform and non-uniform binnings of the packet size distribution for a sampled flow are shown in Figure 1.

The selection of bins can be approached either manually or algorithmically. However, as there are usually multiple classes and a significant number of flows, man ual selection of bin boundaries may be impractical and imprecise. Employing statistical methods for bin selection (or selecting only a subset of the available features) might introduce an improvement over uniform binning. Nonetheless, model-agnostic techniques might fail to capture complex relations between features. Therefore, we propose a flexible, data-aware and model-aware approach.

Innovatively, to determine the binning, we employ Hyperparameter Optimization (HO). In this method, we apply Bayesian optimization methods to optimize the bin boundaries in the training stage. Our results show that our HO method outperforms other optimization methods, such as feature selection and statistical bin selection across all classification tasks, by up to 15% in accuracy. The full description of the proposed method is in Section 4.

Another aspect we optimize is the collection time; that is, the time required for collecting properties from the flow until a classification is made. Many existing approaches classify flows only after they end, after a predefined amount of time has elapsed, or after a specific number of packets have been received. Typically, the collection time is orders of magnitude longer than the inference time, thus dominating the overall classification time.

![](images/6ec97765c1360670ca2bab7c9443e12cccdc0f364a387887c0f5798836fd1ca7.jpg)  
(a) A uniform binning

![](images/b9f059d82e3df07a6778524f71826fa411eb7d14eb0d709a7ab6a3c3465870b3.jpg)  
(b) A non-uniform binning  
Figure 1: A uniform and a non-uniform binning of the packet size distribution of the same example flow. Vertical dotted black lines mark the boundaries of the 5 selected bins. By using non-uniform representations, we can capture more fine-grained details of the flow.

We notice that some flows contain indicative features useful for classification at an early stage, while others require more time for accurate classification. Thus, we introduce Early Classification (EC), a novel setup performing classification in multiple exit times and making a final prediction only upon reaching a certain level of confidence in the classification. Our system is adaptive, classifying some flows at earlier stages, and waiting longer for flows with low confidence in earlier classifications. As our system may invoke multiple classifiers for each flow, we need to create multiple different representations, which might be prohibitive when the number of concurrent flows is large. Consequently, we present a method for creating additive traffic representations, such that the process of updating the representations between classifiers does not incur any additional memory requirements. Additionally, we propose a method that creates tradeoffs between accuracy and collection time, allowing users to tailor these parameters to their specific requirements. The EC setup is presented in Section 5.

In conclusion, this work makes two significant contributions. First, we introduce HO. Our exploration showcases the effectiveness of this strategy, which allows us to improve the classification accuracy by 5%–20% in multiple classification tasks, or, alternatively, reduce memory requirements and computational overheads (as smaller classifiers are required) by 90%.

Our second contribution is by presenting EC, a novel method enabling early traffic classification with an adaptive classification approach. Using this method, the required time for classification can be reduced by up to an order of magnitude, with minimal decline in accuracy, and possibly even an improvement.

Finally, we combine the two methods to create ECHO classifiers, achieving both an accuracy boost of up to 10%, and a reduction in the average collection time by 95%.

The two suggested techniques can be adapted easily to many existing approaches for traffic classification, substantially enhancing their performance.

The rest of this paper is organized as follows: We discuss related work in Section 2. Section 3 explains the networking model and defines the problem of encrypted traffic classification. Section 4 introduces HO, where Bayesian hyperparameter optimization yields non-uniform binnings for packet sizes and arrival times. Section 5 outlines the Early Classification (EC) setup. Subsequently, in Section 6, we present the combined ECHO approach. Finally, Section 7 presents the evaluation results based on three publicly-available datasets, followed by conclusions drawn in Section 8. Note that additional information, including details about our datasets and comparison between different models and representations, is given in the appendices.

## 2 RELATED WORK

Encrypted traffic classification has been extensively studied in recent years (cf. [46, 59] and references therein). Modern classifiers predominantly utilize ML or DL tech niques over representations created from the encrypted traffic. Commonly used representations are statistical features extracted from the traffic [4, 16, 32, 56], timeseries of the first packets of the flow[10, 58], and distributional representations, which include dist [17]—2 pairs of distribution vectors representing packet sizes and arrival times per traffic direction—and flowpic [21, 28, 48]— a two dimensional representation where each element in the matrix captures the number of packet of a certain size arriving at a certain time.<sup>2</sup> Notice that distributional representations often outperform other representations [21] (see further comparison results in Appendix B), and therefore, are employed in this paper.

Many methods and representations require substantial memory and compute resources, which makes them impractical for large networks.

To mitigate the memory and compute requirements, some works (e.g., [13, 19, 20, 27, 40, 47, 51, 56]), have shown how to extract certain features (e.g., flow statistics) from the traffic, or reduce feature dimensionality using feature selection.

Non-uniform binnings (as we suggest in this work) were rarely considered in the context of flow representations. There are two notable works in this area. Barradas et al. [6] have suggested an optimization process that consists of creating uniform binning for packet size distribution and pruning bins using feature selection methods, where the final selection of features is a subset of the original uniform bins. Garcia et al. [24] have proposed a statistical algorithm based on the Kolmogorov-Smirnov statistical test for selecting histogram bins, aiming at maximizing the separation between classes (measured using the Jensen-Shanon Distance).

Our research focuses on the introduction of non-uniform binnings derived by a Bayesian hyperparameter optimization process. We note that in the field of traffic classification, most previous literature regarding Bayesian hyperparameter optimization is focused on selecting hyperparameters for classifiers [8, 9], but not for flow representations. HO, our strategy for creating non-uniform representations, outperforms all previously suggested optimization methods in all explored classification tasks, and can be plugged into many of the previous works to enhance their performance and reduce their memory footprint, as detailed in Section 4.

As for early classification, some works have suggested using the first few packets of the flow for early classification of flows [10–12, 36–38, 54, 58, 60]. While for some classification tasks, the first few packets of a connection suffice, this is not always the case and can lead to less accurate classification [21], this trend is also observable in our experiments (Appendix B).

A first step towards early classification was suggested in [50, 55], where two classifiers are used: the first classifier is based on simpler classification rules, while the second classifier employs more complex rules or a larger model, allowing for more adaptive classification schemes. To the best of our knowledge, in the context of encrypted traffic classification, no extensive research was conducted on building confidence-based classifiers, where a classification is made only after reaching a threshold of certainty.

## 3 PROBLEM STATEMENT

We first describe our networking model and define precisely the problem at hand.

Data is transmitted over the network from a source to a destination as a flow (namely, a timestamped sequence of packets) over communication links. Typically, many flows share the same communication link. Thus, when observing a communication link, we first need to map the packets to their corresponding flows.

We note that flows are commonly defined by a fivetuple (namely, the following five header fields in an IP packet: source and destination IP addresses, source and destination ports, and protocol) [42, 56]. However, this definition is not rigid and can be seamlessly modified to meet different settings or requirements (e.g., in case parts of the five-tuple will be obfuscated in the future or to address a different classification task).

This work focuses on classifying flows that traverse the network. Thus, when aflow (with identifier q) is ini tiated or requires classification, a flow representation $r _ { q }$ is generated to capture relevant properties of q. Since encryption techniques obfuscate most features, we assume only packet sizes, arrival times, and packet directions are available. We aim to classify a large number (namely, millions) of flows simultaneous $\mathsf { l y } ,$ implying that, at any given time, many flow representations are being collected and stored in the system.

Flow information is collected for a predefined time τ, where the representation $r _ { q }$ is built on the fly. Then, $r _ { q }$ is passed to a classifier $f ,$ which predicts the label $f ( r _ { q } )$ of flow $q .$ Upon classification, the appropriate actions may be taken based on the predicted class, such as generating an alert, adding the information to a database, or blocking certain activities. Subsequently, the flow is marked as classified. Alternatively, time-limited classifications can be employed, where the classification remains valid for a specific duration, after which the flow should be reclassified to ensure up-to-date classification results. Figure 2 illustrates the collection and classification process.

![](images/fec07f3fce63dc7fe07287e95187e7e23d859299eae001c76610d15863aef0c0.jpg)  
Figure 2: The key stages in the classification process. Packets are mapped by their flow (the color), and the flow representations are updated accordingly. After a predefined timeout, the flow representation is passed into a classifier to predict the class of the flow (e.g., the used application). Arrows represent the flow of data between the stages, whereas dotted arrows indicate memory access.

## 4 HYPERPARAMETER OPTIMIZATION (HO) OF BINNINGS

In this section, we present HO, a novel strategy to create non-uniform binnings that enable efficient classification. We have explored both non-uniformity in the packet size distribution vector and the arrival-time distribution vector.

Binning consists of reducing the granularity of the representation such that each original value is mapped to a bin. Each bin represents an interval of the original values. Formally, a uniform representation of size N for values in [0, x) represents the data in N bins, where bin $i \in \{ 1 , \ldots , N \}$ is for values in $\big [ \frac { ( i - 1 ) \cdot x } { N } , \frac { i \cdot x } { N } \big )$ . A nonuniform N-bin representation has additional degrees of freedom to choose the boundaries by defining a vector

$$
B = [ b _ {0}, \dots , b _ {N} ],
$$

such that $0 = b _ { 0 } < b _ { 1 } < \ldots < b _ { N - 1 } < b _ { N } = x .$ . In such a representation, bin $i \in \{ 1 , \ldots , N \}$ is for values in $[ b _ { i - 1 } , b _ { i } ) . ^ { 3 }$ In general, we examine two additional properties of binnings: data-aware and model-aware binnings.

Table 1: The different parameters observable by the representation-optimization process

<table><tr><td></td><td>Data-aware</td><td>Variable Sized Bins</td><td>Model-aware</td></tr><tr><td>Uniform</td><td>✗</td><td>✗</td><td>✗</td></tr><tr><td>Feature Selection</td><td>√</td><td>✗</td><td>✗</td></tr><tr><td>Statistical</td><td>√</td><td>√</td><td>✗</td></tr><tr><td>HO</td><td>√</td><td>√</td><td>√</td></tr></table>

A binning is data-aware if, in the creation process, it takes properties of the traffic into account. A simple example of data-aware binning is to employ Feature Selection methods and decide not to store some of the (fixed-sized) bins, based on the data [6].

A more sophisticated data-aware binning is to use Statistical methods to select variable-sized bins (repre sented as a vector B) that create a separation between the distributions of the different classes of the data. Inspired by [24], we use a multiclass version of the Jensen-Shanon distance metric [35], where classes are compared in an one-vs-all manner.

A model-aware binning, which we are first to propose, corresponds to the specific classifier that will eventually use the representations for classification. This approach allows us to tune the representation by the anticipated performance of the final model, distinguishing it from all other binning operations (see Table 1).

Orthogonal to the information available to the binning process is the way the different elements in B are selected, where we distinguish between two approaches. The naive greedy approach (as used, for example, in [24]) iteratively selects a single bin boundary, maximizing the objective function given previous selections.

HO, on the other hand, employs a hyperparameter optimization algorithm for binning selection. Hyperparameter optimization, in general, refers to the process of finding the best combination of hyperparameters (configuration settings that are not learned in the training stage, but rather set before training the classifier) for a given classifier. In our context, the hyperparameters are the selected bins for the representation, the search space includes all possible combinations of bin boundaries, and the objective we aim to maximize in the Bayesian process is the accuracy of a trained model over the validation set. While many hyperparameter optimization approaches exist, we focus on the Tree Parzen Estimators (TPE) method, as it shows superiority over other approaches in past experiments [8, 9].

We note that, unlike [24], we apply TPE also on the Statistical approach, where the objective function corresponds to the Jensen-Shannon distance derived from the possible binnings. While such bin selection is better than the greedy approach, it is still inferior to HO as the Statistical approach is not model-aware.

For the experiments in this work, we use k-fold crossvalidation (KFCV) [31]. Therefore, to validate the TPE process, we use nested cross-validation (NCV) [14], an extension of KFCV for hyperparameter optimization. NCV consists of an outer loop for standard KFCV, selecting training and test sets in each iteration. In the inner loop, we use the training data to iteratively select optimal hyperparameters through another KFCV process. We use $k = 5$ in both the outer and inner loops, implying that for each evaluation in the inner loop, 64% of the flows are used for training, 16% for validating the hyperparameters by calculating the objective function, and 20% for testing (in the outer loop). It is important to note that different iterations of the outer loop might yield different hyperparameter values.

Notice that in our settings, the optimization process is done offline on labeled data, and therefore, has fewer constraints regarding computational power or latency.

Once the optimization process finishes and an optimal result is achieved, the real-time classifier is adapted and uses the optimal hyperparameters (namely, the bin boundaries) achieved by the offline optimizer.

After selecting the bin boundaries, to create our representations without any computational overhead, we create a mapping, using a small direct-access array of size x, between every possible packet size (or discretized arrival time) to its bin index; this implies that the process of building our representations (which is done online, packet by packet) does not incur additional computations (only one memory access).

To capture changes in traffic patterns or in the underlying applications, we propose to run HO periodically, upon degradation of accuracy, or manually if a change in the network condition is known. The process should run in the background without interfering with ongoing classifications.

The results achieved using HO, as well as a comprehensive comparison to the alternative methods, are shown in Section 7.1.

## 5 EARLY CLASSIFICATION (EC) OF TRAFFIC

In this section, we will describe the system setup enabling early traffic classification. EC not only improves the Quality of Service (QoS) and the network security but also saves memory requirements, as flow representations are stored for shorter periods.

This method is based on the assumption that some flows have indicative features at earlier stages and there is no need to wait for a long time to reach an accurate classification. Therefore, in the proposed setup, clas sification occurs upon reaching a sufficient confidence level, without the need to wait several seconds and col lect the full traffic representation. For assessing models confidence, we exploit the fact that many classifiers output the predicted results as a vector $\begin{array} { r } { f ^ { \prime } ( r ) = u , } \end{array}$ where u consists of the predicted probability that a sample is in each class. The predicted class for some sample is then $f ( \boldsymbol { r } ) = \arg \operatorname* { m a x } _ { i = 1 } ^ { C } f ^ { \prime } ( r )$ . For EC, we define the confidence of the classification, denoted by $\beta _ { q } ,$ , as the maximal argument in the resulting vector; namely,

$$
\beta_ {q} = \max _ {i = 1} ^ {C} f ^ {\prime} (r _ {q}).
$$

We note that this approach can be replaced with several different methods for assessing model confidence, as discussed by [33].

The core idea behind EC is that classification occurs in multiple exit times $\tau _ { 1 } , \dots , \tau _ { m a x } ,$ and the final prediction is made when the confidence value exceeds a predefined threshold $\beta ,$ or if the maximal time $\tau _ { m a x }$ has elapsed.

For employing an efficient EC system, we first train (offline) different classifiers $f _ { 1 } , \ldots , f _ { m a x }$ for multiple durations in a logarithmic scale (namely, $\tau _ { i + 1 } = 2 \cdot \tau _ { i } )$ up to the maximal duration $\tau _ { m a x }$ selected for the classification task.

In the online phase, we iteratively build the traffic representations. First, we build the distribution vectors with regard to the first exit time and feed it into the first classifier. If the sample is not classified with sufficient confidence, we keep the packet-sizes distribution vector unchanged and keep collecting packets to it. For the arrival-times distribution vector, in order to adjust the representation to the next classifier, we first merge each bin $2 i - 1$ with its adjacent bin $2 i ,$ leaving the second half of each vector empty. Then, we count arriving packets into the second halves of these vectors, where each bin corresponds to the time that passed since the beginning of the collection process. Formally, for $d ( \tau _ { i } )$ being a distribution vector of the arrival times for the exit time τ (for a single side of the traffic), the values in the updated vector $d ( \tau _ { i + 1 } )$ for the next exit time will be:

<table><tr><td>Times (ms)</td><td>Packet size</td></tr><tr><td>0</td><td>60</td></tr><tr><td>3</td><td>400</td></tr><tr><td>3</td><td>60</td></tr><tr><td>4</td><td>569</td></tr><tr><td>7</td><td>60</td></tr><tr><td>22</td><td>1500</td></tr><tr><td>22</td><td>1500</td></tr><tr><td>23</td><td>60</td></tr><tr><td>23</td><td>64</td></tr><tr><td>23</td><td>60</td></tr><tr><td>33</td><td>420</td></tr></table>

![](images/faacde29b147f13826790e00f51debc5360fe7729891fde027dbd72cb6064778.jpg)  
Figure 3: An illustration of the iterative process of creating the representations for the different time scopes. On the left is an example flow with the arrival times and packet sizes of the first 11 packets. The packetsize boundaries vector is [0, 375, 750, 1125, 1500], the arrival time boundaries vector is dependant on the time scope: $\begin{array} { r l } { [ 0 , \frac { \tau _ { i } } { 4 } , \frac { \tau _ { i } } { 2 } , \frac { 3 \tau _ { i } } { 4 } , \tau _ { i } ] . r _ { q } ^ { ' } ( \tau _ { i } ) } \end{array}$ is the updated representation before adding the packets in the next time interval.

$$
d (\tau_ {i + 1}) _ {j} = \left\{ \begin{array}{l l} d (\tau_ {i}) _ {2 j - 1} + d (\tau_ {i}) _ {2 j} & : j \leq \frac {N}{2} \\ \# (\text { packets   in } [ \frac {j - 1}{N} \cdot 2 \tau_ {i}, \frac {j}{N} \cdot 2 \tau_ {i})) & : \text { else } \end{array} \right..
$$

Using this method, no additional memory is required, and the representations are built and adjusted to the different classifiers on the fly. This process is illustrated in Figure 3.

To minimize the negative effect this process might have on classification, we select the confidence threshold $\beta$ as the accuracy of a baseline model that classifies all flow after τ<sub>max</sub>.

Surprisingly, this scheme not only reduces the average classification time but in some cases also improves the overall classification accuracy. This might occur due to the multiple exit options, allowing the models to identify timely behaviors that are more discernible in earlier classifiers.

Additionally, we explore the tradeoffs between the average collection time and the overall classification accuracy by altering the classification threshold $\beta$ with small α values, making early predictions if the confidence is higher than $\beta - \alpha$

As shown in Appendix B.2, the classification throughput highly depends on the selected classifier and the representation size. Therefore, if EC is deployed on edge devices, at high network rates, or if a strong classifier is selected, there will be a tradeoff between the ability to perform early classification and the rate of classification, as this method requires (possibly) employing multiple classifiers on each flow until it reaches the final prediction. Additionally, as the collection time is significantly higher than the inference time of our classifiers, we neglect the inference time in these comparisons. <sup>4</sup>.

The results exploring EC setups are shown in Section 7.2.

## 6 EARLY CLASSIFICATION WITHHYPERPARAMETER OPTIMIZATION(ECHO)

As we observed that HO improves the performance of models, we wish to create those representations for EC setups as well. For the packet-size distribution vector, we adopt the non-uniform bins of an optimized HO model (a single binning for all classifiers). However, as the arrival time distribution vector are updated in a particular way between EC classifiers (recall Figure 3), customized arrival-times bins cannot be used. The EC setup employing HO on the packet size dimension with uniform time bins is denoted by ECHO.

Yet, we do propose a non-uniform alternative for the arrival time bins, while still maintaining the ability to update the representations in real-time. In this alternative setup, denoted by EC Log, we will use logarithmic bins, that is, for every exit time τ and N bins with boundaries $B = [ b _ { 0 } , \ldots , \dot { b _ { N } } ]$ , where $b _ { 0 } = 0 s , b _ { N } = \tau _ { i }$ , and the other boundaries $( 0 < j < N )$ :

$$
b _ {j} = \tau_ {i} \cdot 2 ^ {- j}.
$$

Using this selection, if the different exit times are defined logarithmically $( \tau _ { i + 1 } = 2 \cdot \tau _ { i } )$ , to update the arrivaltimes vector distribution we simply sum the two values with the smallest indexes, and shift all values one index below. Formally, for $d ( \tau _ { i } )$ being a single distribution vector of arrival times created at time $\tau _ { i } , d ( \tau _ { i + 1 } )$ will be the updated vector for the next classifier:

$$
d (\tau_ {i + 1}) _ {j} = \left\{ \begin{array}{l l} d (\tau_ {i}) _ {1} + d (\tau_ {i}) _ {2} & : j = 1 \\ \# (\text { packets   in } [ \tau_ {i}, \tau_ {i + 1})) & : j = N  . \\ d (\tau_ {i}) _ {j - 1} & : \text { else } \end{array} \right.
$$

In Section 7.3, we have evaluated different selections of packet-size bins for the ECHO setup, and explored the proposed method for the logarithmic arrival-times bins (EC Log).

## 7 EXPERIMENTAL RESULTS

In this section, we provide experimental results investigating the HO strategy for creating efficient traffic representations (Section 4), the EC method for timely traffic classification (Section 5) and the ECHO approach that combines the two strategies (Section 6). We also demonstrate their superiority over alternatives that were previously proposed in the literature.

Our results are structured as follows: First, we examine the effectiveness of HO in traffic classification (Section 7.1). Here, we analyze how the representations created using HO impact classification accuracy and memory utilization. Our investigation highlights the advantages of HO compared to traditional uniform binning and alternative approaches, and provides in-depth insights into the reasons behind the success of the proposed method.

Section 7.2 explores EC methods and how they affect the accuracy and reduce the average collection time of the system.

Finally, we combine the HO method with EC to create efficient classifiers, with high accuracy and with minimal time required for classification (Section 7.3).

In this work, we use the Logistic Regression (LR) [43] classifier for building the models. LR classifiers offer the highest classification throughput compared to other explored classifiers (a detailed comparison in Appendix B), therefore enabling real-time classification for large volumes of traffic. However, we note that in our experiments, similar trends were observed for different ML and DL classifiers.

We use three publicly-available datasets [16, 32, 41, 44], where classification tasks include application identification (e.g., distinguishing between YouTube and Google Music), encryption identification (e.g., distinguishing between different types of VPN), and traffic categorization (e.g. distinguishing between video and VoIP). The different classification tasks we tackle are presented in Table 2, and a thorough description of the datasets, including our preprocessing stage, is in Appendix A.

It is important to note that our preprocessing ensures that the datasets are balanced across all classification tasks, and the difference between accuracy (percentage of correctly classified samples over the test set) and alternative utility metrics (e.g. f1 score, precision, recall) is negligible. Consequently, we evaluate our models and representations based solely on the achieved accuracy using k-fold Cross Validation (KFCV) [31] with k = 5.

Table 2: Different classification tasks we explore. Classification task types are denoted “Apps” for application identification, “Encryption” for encryption identification, and “Categories” for traffic categorization. Additional details appear in Appendix A.

<table><tr><td>Dataset Name</td><td>Task Name</td><td># Classes</td><td>Type</td></tr><tr><td>Quic [44]</td><td>Quic Applications</td><td>5</td><td>Apps</td></tr><tr><td rowspan="3">ISCX combined [16, 32]</td><td>ISCX Applications</td><td>4</td><td>Apps</td></tr><tr><td>ISCX Encryption</td><td>3</td><td>Encryption</td></tr><tr><td>ISCX Categories</td><td>4</td><td>Categories</td></tr><tr><td rowspan="2">VPN Services [41]</td><td>VPN Services</td><td>6</td><td>Encryption</td></tr><tr><td>Streaming or Not</td><td>2</td><td>Categories</td></tr></table>

## 7.1 Hyperparameter Optimization (HO) of Binnings

As observed in our experiments, larger representations improve classification accuracy, but come at the cost of a higher memory footprint and usually more computational requirements.

We compare several methods for selecting binnings over the packet size dimension, including our suggested novel strategy:

Uniform. All bins are of equal size; namely, $\begin{array} { r } { b _ { i } = \frac { i \cdot x } { S } . } \end{array}$ where S is the number of bins.

Feature Selection. Inspired by [6], we employ featureselection methods on larger uniform representations, to create a smaller pruned representation. Given the required number of bins N, we apply feature selection on multiple uniform representations with different original sizes: $\dot { N } ^ { \prime } \in \{ 1 0 , 2 0 , \dot { 5 } 0 , 1 0 0 , 2 0 0 , 5 0 0 , 1 5 0 0 \}$ , and select the model with the highest achieved accuracy. This representation still uses fixed-size bins, however, it is dataaware and selects features with respect to their statistical significance.

Statistical. As explained in Section 4, and inspired by [24], we use the TPE method for optimization of binning, where the objective function is to maximize a multiclass version of the Jensen-Shanon distance metric [35]. This method maximizes the statistical separation between the different classes independently of the selected classifier.

HO Sizes. Our novel strategy employed on the packet size distribution, using the TPE method with the objective being the accuracy of a trained model, as explained in detail in Section 4.

Throughout all our experiments, we set the number of iterations of the TPE method to 200, as we observed convergence in this iterative process. Note that we have also explored greedy sampling methods for hyperparameter selection, where we progressively built the hyperparameter configuration by selecting the option in each subsequent bin that maximized the objective function given the previously chosen options. However, as greedy selection methods do not have as many degrees of freedom, and showed no noticeable advantage over the TPE method, we focus our discussion here on the TPE.

The results are shown in Figure 4. Evidently, the HO Sizes approach is able to capture the nuances and patterns in smaller representations, leading to improved classification accuracy throughout all classification tasks. Additionally, statistical optimization (Statistical) shows an advantage over uniform representations; however, this trend is not consistent for all tasks and sizes. Finally, the Feature Selection method introduces a degradation in accuracy compared to uniform representations. This might be caused by the loss of information in the feature selection process, in the inherent limitation of selecting only sampled features for a single uniform representation (of larger size).

We note that introducing non-uniformity in the packet sizes dimension leads to a significant enhancement in the model’s accuracy, particularly evident when employing the HO Sizes approach. We further explore nonuniformity by introducing non-uniformity in the arrivaltimes dimension. We compare the following representations: Uniform representations, HO Sizes - that use non-uniform bins for the sizes dimension and uniform bins for the arrival-times dimension (as in Figure 4), HO Times - that use non-uniform bins for the arrival time dimension and uniform bins for the sizes dimension, and HO Both that include optimized binning for both dimensions (with different parameters for each dimension). Results are shown in Figure 5. We see that by itself, nonuniformity in the arrival-times dimension shows some advantage over uniform representations. However, this improvement is limited, and when combined with nonuniformity in the packet-sizes dimension, there is little to no advantage in model accuracy compared to HO Sizes.

7.1.1 Explainability. An important property of our binning strategy is its explainability. This is done by looking at the distribution of packet sizes (or arrival times) for each class, and observing what information is given by the new bin boundaries. For example, for the VPN Services task over 5 bins, Figure 6 depicts the selected bin boundaries of one of the runs of HO Sizes, along with the packet sizes distribution of each class. It is easy to

![](images/f3b25834ee0b1a3e1194fe26f1924d25bf7f6d8450d7dca247d571424ab80d41.jpg)  
(a) Quic Applications

![](images/19c406d28b09df702baeb000bb29a66a4f9e9391edc92ff3c752055fd97ae44d.jpg)  
(b) ISCX Applications

![](images/0c3bfde222741f0ee4d89f0428ac712d08fb92e4c52e43d97e085bd4ab8d8953.jpg)  
(c) ISCX Encryption

![](images/5663e01cda6bc976825c1a2b2bb4b545884b99e783f1469e81e99e2be88b7103.jpg)  
(d) ISCX Categories

![](images/aa0034c22ef31a2da5f8563b47db2ab65d48c28c6f399178ede7e93aa625324f.jpg)  
(e) VPN Services

![](images/b862427fbb522c045910e359169d80d5e888b9c7909ead0ae6966a5fc8141b00.jpg)  
(f) Streaming or Not  
Figure 4: Accuracy as a function of the number of bins, for different binning strategies on the packet size dimension. The time dimension binning is uniform in all experiments.

## 7.2 Early Classification (EC) of Traffic

see that bin boundaries are correlated to the data distribution. Specifically, notice that one of the boundaries is at 168 bytes. In retrospect, this appears to distinguish between typical SSTP packets and typical OpenVPN pack ets. Similarly, the bin boundary of 76 bytes appears to distinguish between L2TP IPsec traffic (which has many smaller packets) and WireGuard traffic (with bigger packets). These boundaries demonstrate the strength of the HO approach, as coarse-grained uniform representations commonly group these values together resulting in misclassifications; for example, Figure 7 shows a confusion matrix of a classifier using coarse a flow representation with 5 uniform bins. We can see that the classes that are misclassified are the classes for which the boundaries selected by HO Sizes provide the necessary separation. An optimized representation employing an LR classifier with the same number of bins achieved an accuracy of 98%, in contrast to all other binning methods achieving accuracy lower than 90%, as the Uniform and Feature Selection approaches are limited to bins of equal size, and the bins selected by the Statistical approach were correlated to the overall data distribution but were unable to capture small nuances that affected the final classification performance.

This section explores our EC setup, which is based on training multiple classifiers $f _ { 1 } , \ldots , f _ { m a x }$ for multiple exit times $\tau _ { 1 } , \dots , \tau _ { m a x }$ . When a classifier $f _ { i } \ ( 1 \leq i < m a x )$ achieves a confidence value larger than a threshold $\beta ,$ the classification stops and the label predicted by $f _ { i }$ is reported. Otherwise, after the maximal exit time τ<sub>max</sub>, the label predicted by $f _ { m a x }$ is reported (regardless of its confidence). A detailed explanation can be found in Section 5. In this section, for ease of presentation, we used a pseudo-logarithmic scale (1ms, 2ms, 5ms, 10ms . . .).

First, to gain a sense of the behavior of the confidence for the different classifiers, we train the classifiers $f _ { 1 } , \ldots , f _ { m a x }$ and checked their classification accuracy and coverage (the proportion of instances for which the classifier provides a prediction) for possible confidence thresholds.

The results for a single classification task (namely, VPN Services with 5 bins) are shown in Figure 8. Some significant insights emerge from these results. First, even with short exit times, many samples have been classified with high confidence, thus validating the underlying principle of our method: many flows can be classified at an early stage, thereby reducing the average classification time and saving memory resources. Second, we observe an improvement in model coverage and accuracy over time, indicating that subsequent classifiers generally classify with higher accuracy and cover a broader range of flows. Yet, some flows are correctly classified in earlier classifiers but are misclassified in subsequent ones. This indicates that there are timely features that become hard to recognize after a longer period.

![](images/17425549ab3652817a7494f49226bd1f3c435316759ffdd41f345a0b93782f0b.jpg)  
(a) Quic Applications

![](images/9c9900f49ec16ef09d8f2f864a4aa020e443dc6ed80810073cad0552feb2a49f.jpg)  
(b) ISCX Applications

![](images/8fade5145e62111800d1bf1137e68935f40cf8e92cd8883540a4e358e697f9d7.jpg)  
(c) ISCX Encryption

![](images/01a8d22ebf0fb97564b549b261835a7d15663af44ebcef376f1a3c5e9f13567c.jpg)  
(d) ISCX Categories

![](images/516a2c3dbaf043c33dfc22f90f64582ea6570d1d90090f37ac3568306a544f93.jpg)  
(e) VPN Services

![](images/b3aa48d5f2bf50fb657e79d775d7bbf31ed1f1bcdbbf1e35c27c334d8bf0e91b.jpg)  
(f) Streaming or Not

Figure 5: Accuracy as a function of the number of bins, comparing HO on the different dimensions, as well as on both dimensions.  
![](images/0b3d404122b5ee654b5d8d1be771f694bab2462fd270d98311cf57873b62d403.jpg)  
Figure 6: (a) The entire packet sizes distribution of the VPN dataset with respect to VPN labels; (b) The histogram zoomed in a specific range with the bin boundaries selected by the HO Sizes strategy (for the VPN Services classification task with 5 bins) marked in black. We can see how the selection of bins correlates to the discriminative features of some classes.

Following this experiment, we proceeded to evaluate the EC setup, where we determined the initial classification threshold β based on the accuracy of a baseline model that classifies all flows after the maximal time τ<sub>max</sub>. 5

![](images/f9d1e9f94ef82209a45ef9c44d36bf82964e2e3cfa8384f79d6199b52413e41f.jpg)  
Figure 7: A confusion matrix of an LR classifier using flow representations with 5 uniform bins. Each entry denotes the proportion of flows belonging to a certain class that have been predicted to fall into another class. Notable misclassifications are between L2TP IPsec and WireGuard, as well as between OpenVPN and SSTP.

![](images/1253db7379a9a882d405916876f1c873fb4194deea89b7af922c9941ca59c9a9.jpg)  
Figure 8: Graphs showing coverage and percentage of true and false predictions as a function of the confi dence threshold, for classifiers of different exit times.

For the same classification task as shown in Figure 8 (VPN Services with 5 uniform bins), the EC model results are shown in Figure 9.

We can see two phenomena. First, the average classification time for flows stands at 1.01 seconds, in contrast to the baseline model’s classification time of 5 seconds, representing a notable improvement of approximately 80% in classification speed.

![](images/627971165d1e9a1249ae560a77665ca2e9f2be76de9ab096da3c5752ec03fbfe.jpg)  
Figure 9: The percentage of flows classified up to each period (the coverage) in the EC setup. We can also see the amount of flows classified correctly and incorrectly. The final EC model’s accuracy is marked in red, while the predetermined threshold $\beta$ is marked in green.

![](images/c512560e87cca7b4806c08d68bc69fe86b08c8f82c80f9a8f6a1ec179fa6ef0f.jpg)  
(a) Average Exit Time

![](images/e46eabe3a2e217c9c57218d57720f7b0a35ee4250286998ec42447795a13b580.jpg)  
(b) Accuracy  
Figure 10: The accuracy and the average exit time of EC models with different numbers of bins, across all classification tasks. Results are relative to the maximal time period $\tau _ { m a x }$ and the corresponding classifier $f _ { m a x }$ of each specific classification task and number of bins.

Moreover, the final accuracy of the EC model surpasses that of the baseline model. This means that not only we can save classification time, but EC can potentially improve the model’s accuracy. As previously discussed, this improvement could stem from timely features identified by earlier models, which may go unnoticed by subsequent ones.

![](images/11e51a64d26969e9f6bf5889eb35d29c1e62ec4285570a6566e0550d63b45e0e.jpg)  
Figure 11: The accuracies and the average exit times of EC models with different thresholds, for the VPN Services classification task with 5 bins. $\beta$ is set to be the accuracy of the baseline model, and the threshold for each model is $\beta - \alpha .$ . Notice that the graph’s x-axis is not linear and shows the baseline model that classifies all flows after $\tau _ { m a x } = 5 s$

Figure 10 compares models utilizing EC for different tasks, where each value is normalized against a uniform binning model with the appropriate number of bins. These figures highlight the inherent trade-offs in employing EC: While larger representations facilitate faster classification, there is a slight compromise in accuracy compared to baseline models. On the other hand, smaller representations have the potential to surpass the performance of baseline models, as explained above.

The rationale behind these results lies in the fact that larger representations encapsulate finer details about the flows, thereby boosting the confidence of earlier models. Nevertheless, the notable enhancement in reducing classification time comes with the potential of misclassification at these early stages.

We also compare the results of the EC setup with a lower classification threshold $( \beta - \alpha )$ . The results of this comparison for one classification task are shown in Figure 11.

By opting for a lower threshold, a greater number of flows undergo early-stage classification, thereby reducing the average classification time. However, while the classification time is reduced, there is a notable decrease in accuracy. This tradeoff is controlled by selecting the threshold parameter, giving the flexibility to fine-tune this threshold according to specific requirements and constraints. In this experiment, it is evident that up to an α value of $5 \% ,$ the decline in accuracy is negligible (lower than 1%), while there is a reduction of 25% in collection time.

## 7.3 Early Classification with

## Hyperparameter Optimization (ECHO)

Having noted the effectiveness of HO in enhancing model accuracy (Section 7.1), we aim to extend these representations to EC setups as well.

First, we will compare two methods for the bins of the arrival times distribution, the simple EC with uniform time and size bins, and the EC Log method with logarithmic time bins. The full description of those methods and how they are updated to allow real-time classification without memory overhead is in Section 6.

The comparison results for different numbers of bins and different α values are shown in Figure 12. The results for the two methods are similar. Yet, a noteworthy trend is that with smaller representations, the performance of EC Log is inferior. Conversely, for larger representations, EC Log tends to exhibit higher accuracy, surpassing the accuracy of the uniform EC. We observe that while introducing non-uniformity in the time dimension enhances accuracy, its impact is relatively minor compared to the non-uniformity seen in the packet-sizes dimension, as depicted earlier in Figure 5.

In the following experiment, we evaluate the creation of EC models with non-uniform bins in the packet size dimension, namely ECHO. As explained in Section 6, this process does not require any additional memory or computational power. For the ECHO models in this comparison, $\beta$ is selected as the accuracy of a baseline uniform model, and α is 5% based on previous observations (Figures 11 and 12). The selected α value strikes a balance between average exit time and accuracy, with similar trends noted for other values of .

Figure 13 compares different selections of bins for the EC model, where each selection is based on an HO optimization over a classifier with the corresponding time scope $f _ { 1 } , \ldots , f _ { m a x }$ . Figure 13a compares the accuracy of the ECHO setups, it is noticable that ECHO significantly improves the model’s accuracy compared to the uniform EC model. However, the accuracy results are still lower than an HO setup (with non-uniform packet size bins) that classifies all flows after $\tau _ { m a x }$

Moreover, even though no specific classifier has a clear advantage in average accuracy, there is a smaller standard deviation for subsequent classifiers, implying that the binnings of these classifiers are more reliable and consistent, and therefore, are preferable.

![](images/3a2f86eaa5d7e4c930f5dcd8afbb7e2ce249b51aadb82e1e4cf1f3e822cf677a.jpg)  
(a) VPN Services - 5 bins

![](images/4d4a9c763d4c5a532d7ed0c6cd269cc17a7e6442f909b01ca15f583c908d291e.jpg)  
(b) VPN Services - 10 bins

![](images/ddfd9282bcaf669ae6d0301dc74e95d7a20635eaf654e58d2e09eeee2037c421.jpg)  
(c) VPN Services - 20 bins

![](images/7f8051f526df3c13f26f402f1dd10647f7fd303d833b76d44bcf1b6b9668661a.jpg)  
(d) VPN Services - 50 bins

Figure 12: Accuracy as a function of the average classification time, created using different α values (as in Figure 11). Each graph compares the uniform and the logarithmic methods for creating the bins for the arrival-times dimension for a given number of bins.

![](images/f2e7394cf85ff88ad0e179d8a5392274652ff76486b8fb9c9963c95b3db92b3a.jpg)  
(a) Accuracy

![](images/01c2a78ead122b7b7c6d899293ac673b087f59a20bc86397bfbe7f738ac94e92.jpg)  
(b) Average exit time  
Figure 13: Different bin selection methods for creating ECHO models. Uniform and HO models classify all flows after 5 seconds, while the EC and ECHO models perform early classification. ECHO models have optimized packet size bins based on different exit times. The error bars in the Bayesian results show the standard deviation of the results of the NCV process (see Section 4). Notice that the time-graph’s y-axis is not linear and shows the baseline models (Uniform or ECHO), classifying all flows after $\tau _ { m a x } = 5$

In Figure 13b, we compare the same classifiers in terms of average exit time. Here, for all binnings, the ECHO models show significantly faster average classification times (with no advantage to any specific selection). Recall that the threshold value for the EC models is based on a baseline uniform model, and as shown earlier, HO significantly improves accuracy, which is then reflected as well in higher confidence in classification. Thus enabling faster classification but with a lower accuracy than a full HO model.

## 8 CONCLUSIONS

This paper highlights the fact that many traffic classification techniques have considerable room for improvement. The techniques applied in the ECHO approach can seamlessly be combined with many existing traffic classification methods, and reduce both their memory footprint and their collection time without compromising any aspect of the classification process.

We show that by employing hyperparameter optimization methods to create non-uniform flow representations, we can significantly reduce the memory over head of representations without compromising model accuracy. Furthermore, it boosts the model’s throughput as smaller and more efficient classifiers are used.

We also demonstrate that building a setup that includes multiple exit times with multiple classifiers, can significantly reduce the average required time for classification with no additional memory requirements.

In this paper, we utilize the TPE algorithm to opti mize the variable-sized bins. Although this process is conducted offline, in future work, we aim to investigate other methods with improved time efficiency. We also wish to explore whether other flow representations could be optimized in terms of memory usage.

In addition, we aim to delve into different methods to create the setup for early traffic classification, and different methods for assessing the models’ confidence as part of the early classification process.

## 8.1 Reproducability

Our code, as well as the processed datasets, will be publicly available to the community upon completion of the double-blind review process of our paper.

## 8.2 Acknowledgments

Part of this work has been supported by Israel Innovation Authority within the ENTM consortium.

## REFERENCES

[1] Giuseppe Aceto, Domenico Ciuonzo, Antonio Montieri, and Antonio Pescapè. 2019. MIMETIC: Mobile encrypted traffic classification using multimodal deep learning. Computer Networks 165 (2019), 106944.

[2] Giuseppe Aceto, Alberto Dainotti, Walter de Donato, and Antonio Pescapé. 2010. PortLoad: Taking the Best of Two Worlds in Traffic Classification. 2010 INFOCOM IEEE Conference on Computer Communications Workshops (2010), 1–5.

[3] Iman Akbari, Mohammad A. Salahuddin, Leni Ven, Noura Li mam, Raouf Boutaba, Bertrand Mathieu, Stephanie Moteau, and Stephane Tuffin. 2021. A Look Behind the Curtain: Traffic Classification in an Increasingly Encrypted Web. Proc. ACM Meas. Anal. Comput. Syst. 5, 1, Article 04 (feb 2021), 26 pages.

[4] Blake Anderson and David McGrew. 2017. Machine Learning for Encrypted Malware Traffic Classification: Accounting for Noisy Labels and Non-Stationarity. In KDD’17. 1723–1732. https: //doi.org/10.1145/3097983.3098163

[5] Anonymous. 2023. Private Communincation..

[6] Diogo Barradas, Nuno Santos, Luís Rodrigues, Salvatore Signorello, Fernando M. V. Ramos, and André Madeira. 2021. FlowLens: Enabling Efficient Flow Classification for ML-based Network Security Applications. In NDSS’21.

[7] Gustavo E. A. P. A. Batista, Ronaldo C. Prati, and Maria Carolina Monard. 2004. A Study of the Behavior of Several Methods for Balancing Machine Learning Training Data. SIGKDD Explor. Newsl. 6, 1 (jun 2004), 20–29. https://doi.org/10.1145/1007730. 1007735

[8] James Bergstra, Rémi Bardenet, Yoshua Bengio, and Balázs Kégl. 2011. Algorithms for Hyper-Parameter Optimization. In Advances in Neural Information Processing Systems, Vol. 24.

[9] James Bergstra, Daniel Yamins, and David Cox. 2013. Making a Science of Model Search: Hyperparameter Optimization in Hundreds of Dimensions for Vision Architectures. In ICML’13 (Proceedings of Machine Learning Research, Vol. 28). PMLR, 115– 123.

[10] Laurent Bernaille, Renata Teixeira, Ismael Akodkenou, Augustin Soule, and Kave Salamatian. 2006. Traffic Classification on the Fly. SIGCOMM Comput. Commun. Rev. 36, 2 (apr 2006), 23–26.

[11] Laurent Bernaille, Renata Teixeira, Ismael Akodkenou, Augustin Soule, and Kave Salamatian. 2006. Traffic classification on the fly. SIGCOMM Comput. Commun. Rev. 36, 2 (apr 2006), 23–26. https://doi.org/10.1145/1129582.1129589

[12] Laurent Bernaille, Renata Cruz Teixeira, and Kave Salamatian. 2006. Early application identification. In Conference on Emerging Network Experiment and Technology. https://api.semanticscholar. org/CorpusID:496969

[13] Francesco Bronzino, Paul Schmitt, Sara Ayoubi, Hyojoon Kim, Renata Teixeira, and Nick Feamster. 2021. Traffic Refinery: Cost-Aware Data Representation for Machine Learning on Network Traffic. Proc. ACM Meas. Anal. Comput. Syst. 5, 3, Article 40 (dec 2021), 24 pages.

[14] Gavin C. Cawley and Nicola L.C. Talbot. 2010. On Over-Fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. J. Mach. Learn. Res. 11 (aug 2010), 2079–2107.

[15] Corinna Cortes and Vladimir Naumovich Vapnik. 1995. Support-Vector Networks. Machine Learning 20 (1995), 273–297.

[16] Gerard Draper-Gil, Arash Habibi Lashkari, Mohammad Saiful Islam Mamun, and Ali A Ghorbani. 2016. Characterization of encrypted and VPN traffic using time-related features. In ICISSP. 407–414.

[17] Aviv Engelberg and Avishai Wool. 2021. Classification of Encrypted IoT Traffic Despite Padding and Shaping. arXiv:2110.11188 [cs.CR] https://arxiv.org/abs/2110.11188

[18] Reese Enghardt, Tommy Pauly, Colin Perkins, Kyle Rose, and Christopher A. Wood. 2020. A Survey of the Interaction between Security Protocols and Transport Services. RFC 8922.

[19] Fatih Ertam and Engin Avcı. 2017. A new approach for internet traffic classification: GA-WK-ELM. Measurement 95 (2017), 135– 142. https://doi.org/10.1016/j.measurement.2016.10.001

[20] Adil Fahad, Zahir Tari, Ibrahim Khalil, Ibrahim Habib, and Hussein Alnuweiri. 2013. Toward an efficient and scalable feature selection approach for internet traffic classification. Computer Networks 57, 9 (2013), 2040–2057. https://doi.org/10.1016/j. comnet.2013.04.005

[21] Alessandro Finamore, Chao Wang, Jonatan Krolikowski, José Manuel Navarro, Fuxing Chen, and Dario Rossi. 2023. Replication: Contrastive Learning and Data Augmentation in Traffic Classification Using a Flowpic Input Representation. Proceedings of the 2023 ACM on Internet Measurement Conference (2023). https://api.semanticscholar.org/CorpusID:262046478

[22] Michael Finsterbusch, Chris Richter, Eduardo Rocha, Jean Alexander Muller, and Klaus Hanssgen. 2014. A Survey of Payload-Based Traffic Classification Approaches. IEEE Com munications Surveys & Tutorials 16, 2 (2014), 1135–1156. https: //doi.org/10.1109/SURV.2013.100613.00161

[23] Kunihiko Fukushima. 1980. Neocognitron: A self-organizing neural network model for a mechanism of pattern recognition unaffected by shift in position. Biological Cybernetics 36 (1980), 193–202.

[24] Johan Garcia and Topi Korhonen. 2018. Efficient Distribution-Derived Features for High-Speed Encrypted Flow Classification. Proceedings of the 2018 Workshop on Network Meets AI & ML (2018). https://api.semanticscholar.org/CorpusID:51929029

[25] Patrick Haffner, Subhabrata Sen, Oliver Spatscheck, and Dong mei Wang. 2005. ACAS: Automated Construction of Application Signatures. In ACM SIGCOMM MineNet’05. 197–202.

[26] Tin Kam Ho. 1995. Random decision forests. In Proceedings of 3rd International Conference on Document Analysis and Recognition, Vol. 1. 278–282 vol.1. https://doi.org/10.1109/ICDAR.1995. 598994

[27] Jordan Holland, Paul Schmitt, Nick Feamster, and Prateek Mittal. 2021. New Directions in Automated Traffic Analysis. In ACM CCS’21. 3366–3383.

[28] Eyal Horowicz, Tal Shapira, and Yuval Shavitt. 2022. A Few Shots Traffic Classification with Mini-FlowPic Augmentations. In ACM IMC’22 (Nice, France). 647–654. https://doi.org/10. 1145/3517745.3561436

[29] Gordon P. Hughes. 1968. On the mean accuracy of statistical pattern recognizers. IEEE Trans. Inf. Theory 14 (1968), 55–63. https://api.semanticscholar.org/CorpusID:206729491

[30] Arthur S. Jacobs, Roman Beltiukov, Walter Willinger, Ronaldo A. Ferreira, Arpit Gupta, and Lisandro Z. Granville. 2022. AI/ML for Network Security: The Emperor Has No Clothes. In Proceed ings of the 2022 ACM SIGSAC Conference on Computer and Com munications Security (Los Angeles, CA, USA) (CCS ’22). Association for Computing Machinery, New York, NY, USA, 1537–1551. https://doi.org/10.1145/3548606.3560609

[31] Ron Kohavi. 1995. A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection. In International Joint Conference on Artificial Intelligence.

[32] Arash Habibi Lashkari, Gerard Draper-Gil, Mohammad Saiful Islam Mamun, and Ali A. Ghorbani. 2017. Characterization of Tor Traffic using Time based Features. In ICISSP.

[33] JING LEI. 2014. Classification with confidence. Biometrika 101, 4 (2014), 755–769. http://www.jstor.org/stable/43304686

[34] Rui Li, Xi Xiao, Shiguang Ni, Haitao Zheng, and Shutao Xia. 2018. Byte Segment Neural Network for Network Traffic Classifi cation. 2018 IEEE/ACM 26th International Symposium on Quality of Service (IWQoS) (2018), 1–10. https://api.semanticscholar.org/ CorpusID:59232416

[35] Jianhua Lin. 1991. Divergence measures based on the Shannon entropy. IEEE Trans. Inf. Theory 37 (1991), 145–151. https://api. semanticscholar.org/CorpusID:12121632

[36] Chang Liu, Longtao He, Gang Xiong, Zigang Cao, and Zhen Li. 2019. FS-Net: A Flow Sequence Network For Encrypted Traffic Classification. IEEE INFOCOM 2019 - IEEE Conference on Computer Communications (2019), 1171–1179. https://api. semanticscholar.org/CorpusID:86515190

[37] Manuel Lopez-Martin, Belen Carro, Antonio Sanchez Esguevillas, and Jaime Lloret. 2017. Network Traffic Classifier With Convolutional and Recurrent Neural Networks for Internet of Things. IEEE Access 5 (2017), 18042–18050.

https://doi.org/10.1109/ACCESS.2017.2747560

[38] Mohammad Lotfollahi, Mahdi Jafari Siavoshani, Ramin Shirali Hossein Zade, and Mohammdsadegh Saberian. 2017. Deep packet: a novel approach for encrypted traffic classification using deep learning. Soft Computing 24 (2017), 1999 – 2012. https://api.semanticscholar.org/CorpusID:35187639

[39] Andrew W. Moore and Konstantina Papagiannaki. 2005. Toward the Accurate Identification of Network Applications. In PAM’05. 41–54.

[40] Andrew W. Moore and Denis Zuev. 2005. Internet Traffic Classification Using Bayesian Analysis Techniques. SIGMETRICS Perform. Eval. Rev. 33, 1 (jun 2005), 50–60.

[41] Mohamed Naas and Jan Fesl. 2023. A novel dataset for encrypted virtual private network traffic analysis. Data in Brief 47 (2023), 108945.

[42] Thuy T.T. Nguyen and Grenville Armitage. 2008. A survey of techniques for internet traffic classification using machine learning. IEEE Communications Surveys & Tutorials 10, 4 (2008), 56–76. https://doi.org/10.1109/SURV.2008.080406

[43] Raymond Pearl and Lowell J. Reed. 1920. On the Rate of Growth of the Population of the United States since 1790 and Its Mathematical Representation1. Proceedings of the National Academy of Sciences 6, 6 (1920), 275–288. https://doi.org/10.1073/pnas.6.6. 275

[44] Shahbaz Rezaei and Xin Liu. 2020. How to Achieve High Classification Accuracy with Just a Few Labels: A Semi-supervised Approach Using Sampled Packets. arXiv:1812.09761 [cs.NI] https://arxiv.org/abs/1812.09761

[45] Matthew Roughan, Subhabrata Sen, Oliver Spatscheck, and Nick G. Duffield. 2004. Class-of-service mapping for QoS: a statistical signature-based approach to IP traffic classification. In ACM/SIGCOMM Internet Measurement Conference.

[46] Ola Salman, Imad H Elhajj, Ayman Kayssi, and Ali Chehab. 2020. A review on machine learning–based approaches for Internet traffic classification. Annals of Telecommunications 75, 11 (2020), 673–710.

[47] Muhammad Shafiq, Xiangzhan Yu, Ali Kashif Bashir, Hassan Nazeer Chaudhry, and Dawei Wang. 2018. A machine learning approach for feature selection traffic classification using security analysis. The Journal of Supercomputing 74 (2018), 4867–4892.

[48] Tal Shapira and Yuval Shavitt. 2019. Flowpic: Encrypted internet traffic classification is as easy as image recognition. In IEEE Infocom Workshops. 680–687.

[49] Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani. 2018. Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. In ICISSP.

[50] Arunan Sivanathan, Hassan Habibi Gharakheili, Franco Loi, Adam Radford, Chamith Wijenayake, Arun Vishwanath, and Vijay Sivaraman. 2019. Classifying IoT Devices in Smart Environments Using Network Traffic Characteristics. IEEE Transactions on Mobile Computing 18 (2019), 1745–1759. https://api. semanticscholar.org/CorpusID:70082542

[51] Thijs van Ede, Riccardo Bortolameotti, Andrea Continella, Jingjing Ren, Daniel J. Dubois, Martina Lindorfer, David R. Choffnes, Maarten van Steen, and Andreas Peter. 2020. Flow-Print: Semi-Supervised Mobile-App Fingerprinting on Encrypted Network Traffic. Proceedings 2020 Network and Distributed System Security Symposium (2020). https://api.semanticscholar. org/CorpusID:211265114

[52] Wei Wang, Yiqiang Sheng, Jinlin Wang, Xuewen Zeng, Xiaozhou Ye, Yongzhong Huang, and Ming Zhu. 2018. HAST-IDS: Learn ing Hierarchical Spatial-Temporal Features Using Deep Neural Networks to Improve Intrusion Detection. IEEE Access 6 (2018), 1792–1806. https://doi.org/10.1109/ACCESS.2017.2780250

[53] Wei Wang, Ming Zhu, Jinlin Wang, Xuewen Zeng, and Zhongzhen Yang. 2017. End-to-end encrypted traffic classifi cation with one-dimensional convolution neural networks. In 2017 IEEE International Conference on Intelligence and Security In formatics (ISI). 43–48. https://doi.org/10.1109/ISI.2017.8004872

[54] Wei Wang, Ming Zhu, Jinlin Wang, Xuewen Zeng, and Zhongzhen Yang. 2017. End-to-end encrypted traffic classifi cation with one-dimensional convolution neural networks. 2017 IEEE International Conference on Intelligence and Security Infor matics (ISI) (2017), 43–48. https://api.semanticscholar.org/ CorpusID:3720713

[55] Yipeng Wang, Huijie He, Yingxu Lai, and Alex X. Liu. 2023. A Two-Phase Approach to Fast and Accurate Classification of Encrypted Traffic. IEEE/ACM Transactions on Networking 31, 3 (2023), 1071–1086. https://doi.org/10.1109/TNET.2022.3209979

[56] Nigel Williams, Sebastian Zander, and Grenville Armitage. 2006. A preliminary performance comparison of five machine learning algorithms for practical IP traffic flow classification. SIGCOMM Comput. Commun. Rev. 36 (10 2006), 5–16. https://doi.org/10. 1145/1163593.1163596

[57] Yuwei Xu, Jie Cao, Kehui Song, Qiao Xiang, and Guang Cheng. 2023. FastTraffic: A lightweight method for encrypted traffic fast classification. Computer Networks 235 (2023), 109965. https: //doi.org/10.1016/j.comnet.2023.109965

[58] Lixuan Yang, Alessandro Finamore, Feng Jun, and Dario Rossi. 2021. Deep Learning and Zero-Day Traffic Classification: Lessons Learned From a Commercial-Grade Dataset. IEEE TNSM 18, 4 (2021), 4103–4118. https://doi.org/10.1109/TNSM.2021. 3122940

[59] Jingjing Zhao, Xuyang Jing, and Witold Pedrycz. 2021. Network traffic classification for data fusion: A survey. Information Fusion 72 (02 2021). https://doi.org/10.1016/j.inffus.2021.02.009

[60] Zhuang Zou, Jingguo Ge, Hongbo Zheng, Yulei Wu, Chunjing Han, and Zhongjiang Yao. 2018. Encrypted Traffic Classifica tion with a Convolutional Long Short-Term Memory Neural Network. 2018 IEEE 20th International Conference on High Per formance Computing and Communications; IEEE 16th International Conference on Smart City; IEEE 4th International Conference on Data Science and Systems (HPCC/SmartCity/DSS) (2018), 329–334. https://api.semanticscholar.org/CorpusID:59233070

## A DATASETS

This section provides an overview of the three publicly available datasets used for training and testing our models, and the different classification tasks for each dataset.

Quic traffic dataset [44]. The Quic traffic dataset was recorded at UC Davis and consists of the traffic of 5 Google services (Google Drive, YouTube, Google Docs, Google Search, and Google Music) under several operating systems (including different Windows and Ubuntu distributions). The flow counts are shown in Table 3.

Table 3: The number of flows per application in the Quic traffic dataset.

<table><tr><td>Application</td><td>Number of Flows</td></tr><tr><td>Google Search</td><td>1915</td></tr><tr><td>Google Drive</td><td>1636</td></tr><tr><td>Google Doc</td><td>1221</td></tr><tr><td>Youtube</td><td>1077</td></tr><tr><td>Google Music</td><td>592</td></tr></table>

Table 4: The number of flows per category and encryption technique in the ISCX combined traffic dataset.

<table><tr><td>Category</td><td>Non-VPN</td><td>VPN</td><td>Tor</td></tr><tr><td>Voip</td><td>4397</td><td>1543</td><td>1761</td></tr><tr><td>Video</td><td>1180</td><td>301</td><td>438</td></tr><tr><td>File Transfer</td><td>954</td><td>303</td><td>546</td></tr><tr><td>Browsing</td><td>757</td><td>-</td><td>448</td></tr></table>

For this dataset, we consider one classification task, which we call Quic Applications, of classifying flows to one of the different applications.

ISCX combined traffic dataset. This dataset consists of 2 network captures produced by the University of New Brunswick [16, 32]. The captures were filtered to include only the traffic related to the actual label of the flow. Classes with an insufficient number of samples (e.g., chat) were discarded. The processed dataset consists of 4 traffic categories (VoIP, video, file transfer, and browsing) with different applications for each category.

For these categories, we have 3 encryption techniques: non-VPN, VPN (for all classes except browsing), and TOR. As proposed in the original papers, the dataset is sampled using a 15-second non-overlapping time window and every sample is issued as a different flow. Table 4 shows the number of flows for each category and each type of encryption, while Table 5 delves into specific applications within the video and VoIP categories.

For this dataset, we consider three classification tasks: (i) ISCX Applications in which we classify the different applications in Table 5; (ii) ISCX Encryption, in which we classify the different encryption protocols (namely, VPN, Non-VPN, or TOR); and (iii) ISCX Categories, in which we obtain the category (namely, video, VoIP, file transfer, or browsing) for the flow.

VPN services dataset [41]. This dataset consists of packet captures produced and processed by the University of South Bohemia. The processed dataset contains 5 traffic categories (email, video conferencing, SSH, streaming, and non-streaming) using different applications for the streaming and non-streaming categories (the specific applications are not available in the dataset). Traffic from all categories is recorded over VPN and non-VPN connections, and using 7 different VPN settings (L2TP, L2TP IPsec, OpenVPN, PPTP, SSTP, WireGuard, and non-VPN).

Table 5: The number of flows per application in the ISCX traffic dataset (Non-VPN).

<table><tr><td>Category</td><td>Application</td><td>Number of flows</td></tr><tr><td rowspan="4">VoIP</td><td>Facebook</td><td>1997</td></tr><tr><td>Hangout</td><td>2441</td></tr><tr><td>Skype</td><td>1823</td></tr><tr><td>Voipbuster</td><td>1032</td></tr><tr><td rowspan="6">Video</td><td>Vimeo</td><td>565</td></tr><tr><td>YouTube</td><td>534</td></tr><tr><td>Hangouts</td><td>227</td></tr><tr><td>Skype</td><td>210</td></tr><tr><td>Netflix</td><td>207</td></tr><tr><td>Facebook</td><td>176</td></tr></table>

Table 6: The number of flow by category and VPN service in the VPN service dataset [41].

<table><tr><td>VPN Protocol</td><td>non-streaming</td><td>streaming</td></tr><tr><td>L2TP</td><td>1003</td><td>94</td></tr><tr><td>L2TP IPsec</td><td>1003</td><td>93</td></tr><tr><td>Non VPN</td><td>3277</td><td>440</td></tr><tr><td>OpenVPN</td><td>999</td><td>96</td></tr><tr><td>SSTP</td><td>986</td><td>97</td></tr><tr><td>WireGuard</td><td>1003</td><td>99</td></tr></table>

Since the dataset contains a low volume of email, video conferencing, and SSH traffic, we only use the streaming and non-streaming categories. We also ex clude the traffic recorded over PPTP VPN as it contains significantly fewer samples than the other VPN services. The number of flows in each category for the filtered dataset is shown in Table 6. For this dataset, we consider two classification tasks. First, VPN Services, is the task of classifying the specific VPN in use. Secondly, Streaming or Not is the binary task of categorizing the flows of the dataset into streaming/non-streaming categories.

## A.1 Preprocessing

We filter the samples using three parameters: minimal number of packets, minimal volume (in bytes), and minimal duration. For every dataset, we have selected these parameters with regard to similar experiments done in the literature and to our observations of the traffic patterns. The selected parameters for each dataset are shown in Table 7. Additionally, as some of our datasets are imbalanced, we have employed random undersampling [7] to balance the data. This balancing procedure was applied to both the training and test sets to ensure equal representation of each class.

Table 7: Preprocessing parameters

<table><tr><td></td><td>Timeout τ</td><td>Min. Packets</td><td>Min. Vol.</td><td>Min. Dur.</td></tr><tr><td>QUIC</td><td>1s</td><td>10</td><td>0</td><td>0.5s</td></tr><tr><td>VPN</td><td>5s</td><td>100</td><td>10KB</td><td>3s</td></tr><tr><td>ISCX</td><td>15s</td><td>100</td><td>10KB</td><td>5s</td></tr></table>

## B REPRESENTATIONS AND MODELS COMPARISON

In this section, we thoroughly compare different representations with various sizes (detailed below), employing 4 different classifiers, Random Forest (RF) [26], Logistic Regression (LR) [43], Support Vector Machine (SVM) [15], and Convolutional Neural Networks (CNNs, denoted here by DEEP) [23]. Although ECHO can work with any distributional representation and classifier, this comparison justify our selection of representation and model in Section 7.

Recall that we denote the selected representation type as r, where $r _ { q }$ is the calculated representation for the flow with identifier q. We compare the following four common types of flow representations.

Distribution vectors, denoted by dist(N). This representation consists of 4 distribution vectors of size $N ,$ containing, for each flow direction, counters of the arrival times and packet sizes, where each value is mapped to one of the N bins, as suggested by [17]. dist(N) works under the classifiers DEEP 1D-CNN, RF, LR, and SVM. The size of dist(N) is 4N bytes as we store 4 vectors of size N, using 8-bit integers.

Time series, denoted by ts(N). Time series of arrival time, packet size, and packet direction of N packets, as proposed by [10, 58]. ts(N) works under the classifiers DEEP 1D-CNN, RF, LR, and SVM. The size of ts(N) is approximately 6N bytes as we store the arrival time (a 32-bit float), packet size (11 bits for sizes up to 1500), and direction (a boolean value) of N packets.

FlowPic, denoted by $f p ( N \times N )$ . The FlowPic representation is a two-dimensional distribution matrix of size N × N of arrival times and packet sizes, as proposed by [17, 21, 28, 48]. As in dist(N), each packet size and arrival time is mapped to one of N bins. Then, el ement $( i , j )$ in the matrix holds the number of packets whose arrival times are mapped to (arrival time) bin i, and packet sizes are mapped to (packet size) bin j.

Table 8: QUIC Applications classification task.

<table><tr><td></td><td>RF</td><td>SVM</td><td>LR</td><td>DEEP</td></tr><tr><td>dist(5)</td><td>94.9%</td><td>82.7%</td><td>93.6%</td><td>-</td></tr><tr><td>dist(10)</td><td>95.9%</td><td>82.3%</td><td>95.5%</td><td>-</td></tr><tr><td>dist(20)</td><td>95.9%</td><td>82.2%</td><td>95.7%</td><td>94.9%</td></tr><tr><td>dist(50)</td><td>95.7%</td><td>79.4%</td><td>94.4%</td><td>96.2%</td></tr><tr><td>ts(5)</td><td>94.6%</td><td>81.3%</td><td>81.2%</td><td>-</td></tr><tr><td>ts(10)</td><td>95.1%</td><td>80.5%</td><td>79.3%</td><td>-</td></tr><tr><td>ts(20)</td><td>95.3%</td><td>84.5%</td><td>79.7%</td><td>94.7%</td></tr><tr><td>ts(50)</td><td>95.8%</td><td>85.5%</td><td>83.8%</td><td>93.3%</td></tr><tr><td>fp(8)</td><td>93.0%</td><td>78.7%</td><td>95.5%</td><td>95.2%</td></tr><tr><td>fp(16)</td><td>91.8%</td><td>69.8%</td><td>94.7%</td><td>94.7%</td></tr><tr><td>fp(32)</td><td>90.0%</td><td>66.9%</td><td>92.5%</td><td>95.5%</td></tr><tr><td>sts()</td><td>95.0%</td><td>82.9%</td><td>90.0%</td><td>-</td></tr></table>

$f p ( N \times N )$ can be used under the classifiers DEEP 2D-CNN, RF, LR, and SVM. The size of $f p ( N \times N )$ is $2 \cdot N ^ { 2 }$ bytes as we store a two-dimensional vector of size N for each traffic side, using 8-bit integers.

Statistical Features, denoted by sts. Statistical representation, containing 33 basic statistical features, as proposed by [4, 16, 32, 56] and others. The features are the basic minimum, maximum, mean, median, and stan dard deviation of the packet sizes and packet relative arrival times, for all packets and each traffic direction independently, as well as the number of packets for each direction. This representation is only used with simpler ML classifiers: RF, LR, and SVM. The size of sts is 132 bytes if all statistics are stored as 32-bit float values (this can be reduced by setting specific types to each value)<sup>6</sup>.

## B.1 Flow Representations

The results for the different classification tasks are shown in Tables 8–13. For brevity, we show only the accuracy and exclude the std results of the k-fold process. Additionally, we note that the neural network architecture of the DEEP CNNs is not relevant for small dist and ts representations (as it includes pooling layers), as well as sts representations (which have no temporal structure).

We observe some common trends for most of the tasks and representations:

Table 9: ISCX Applications classification task.

<table><tr><td></td><td>RF</td><td>SVM</td><td>LR</td><td>DEEP</td></tr><tr><td>dist(5)</td><td>80.9%</td><td>73.3%</td><td>76.4%</td><td>-</td></tr><tr><td>dist(10)</td><td>87.0%</td><td>79.9%</td><td>91.8%</td><td>-</td></tr><tr><td>dist(20)</td><td>87.3%</td><td>82.8%</td><td>93.4%</td><td>95.9%</td></tr><tr><td> $\underline{dist(50)}$ </td><td>88.8%</td><td>91.7%</td><td>95.6%</td><td>97.8%</td></tr><tr><td>ts(5)</td><td>67.0%</td><td>49.5%</td><td>39.1%</td><td>-</td></tr><tr><td>ts(10)</td><td>68.5%</td><td>56.2%</td><td>42.9%</td><td>-</td></tr><tr><td>ts(20)</td><td>69.6%</td><td>60.1%</td><td>42.8%</td><td>53.5%</td></tr><tr><td>ts(50)</td><td>73.7%</td><td>61.1%</td><td>42.3%</td><td>73.9%</td></tr><tr><td>fp(8)</td><td>80.4%</td><td>72.3%</td><td>77.0%</td><td>78.0%</td></tr><tr><td>fp(16)</td><td>81.4%</td><td>74.9%</td><td>82.6%</td><td>91.4%</td></tr><tr><td>fp(32)</td><td>83.0%</td><td>85.3%</td><td>84.2%</td><td>94.5%</td></tr><tr><td>sts()</td><td>92.8%</td><td>69.3%</td><td>92.9%</td><td>-</td></tr></table>

Table 10: ISCX Encryption classification task.

<table><tr><td></td><td>RF</td><td>SVM</td><td>LR</td><td>DEEP</td></tr><tr><td>dist(5)</td><td>92.3%</td><td>83.6%</td><td>81.1%</td><td>-</td></tr><tr><td>dist(10)</td><td>92.7%</td><td>85.5%</td><td>84.1%</td><td>-</td></tr><tr><td>dist(20)</td><td>92.8%</td><td>88.6%</td><td>90.2%</td><td>94.6%</td></tr><tr><td> $\underline{dist(50)}$ </td><td>90.8%</td><td>93.3%</td><td>91.6%</td><td>96.2%</td></tr><tr><td>ts(5)</td><td>81.2%</td><td>68.3%</td><td>60.8%</td><td>-</td></tr><tr><td>ts(10)</td><td>81.9%</td><td>69.8%</td><td>59.0%</td><td>-</td></tr><tr><td>ts(20)</td><td>83.0%</td><td>69.8%</td><td>58.0%</td><td>82.9%</td></tr><tr><td>ts(50)</td><td>84.6%</td><td>69.8%</td><td>58.3%</td><td>84.5%</td></tr><tr><td>fp(8)</td><td>90.7%</td><td>81.2%</td><td>84.5%</td><td>85.5%</td></tr><tr><td>fp(16)</td><td>92.1%</td><td>83.3%</td><td>88.4%</td><td>93.2%</td></tr><tr><td>fp(32)</td><td>85.4%</td><td>81.4%</td><td>88.1%</td><td>92.7%</td></tr><tr><td>sts()</td><td>95.2%</td><td>78.4%</td><td>82.5%</td><td>-</td></tr></table>

Table 11: ISCX Categories classification task.

<table><tr><td></td><td>RF</td><td>SVM</td><td>LR</td><td>DEEP</td></tr><tr><td>dist(5)</td><td>89.1%</td><td>88.5%</td><td>82.6%</td><td>-</td></tr><tr><td>dist(10)</td><td>90.6%</td><td>89.5%</td><td>89.4%</td><td>-</td></tr><tr><td>dist(20)</td><td>91.1%</td><td>90.6%</td><td>93.3%</td><td>93.2%</td></tr><tr><td>dist(50)</td><td>89.4%</td><td>92.0%</td><td>91.5%</td><td>94.7%</td></tr><tr><td>ts(5)</td><td>77.3%</td><td>62.4%</td><td>55.3%</td><td>-</td></tr><tr><td>ts(10)</td><td>77.9%</td><td>68.1%</td><td>61.5%</td><td>-</td></tr><tr><td>ts(20)</td><td>76.7%</td><td>72.8%</td><td>64.1%</td><td>78.3%</td></tr><tr><td>ts(50)</td><td>76.5%</td><td>75.5%</td><td>63.9%</td><td>82.7%</td></tr><tr><td>fp(8)</td><td>85.8%</td><td>89.0%</td><td>87.6%</td><td>92.2%</td></tr><tr><td>fp(16)</td><td>83.1%</td><td>89.7%</td><td>88.7%</td><td>93.6%</td></tr><tr><td>fp(32)</td><td>80.7%</td><td>88.2%</td><td>88.5%</td><td>94.7%</td></tr><tr><td>sts()</td><td>92.3%</td><td>82.6%</td><td>86.5%</td><td>-</td></tr></table>

First, dist representations achieve the highest accuracy for most classification tasks (with two anomalies favoring f p), with the DEEP CNN classifier achieving the highest accuracy. It is apparent that the distributional features in dist and $f p$ representations hold meaningful information for classification more than raw values as a time series or a collection of statistical values.

Table 12: VPN Services classification task.

<table><tr><td></td><td>RF</td><td>SVM</td><td>LR</td><td>DEEP</td></tr><tr><td>dist(5)</td><td>90.3%</td><td>86.5%</td><td>82.3%</td><td>-</td></tr><tr><td>dist(10)</td><td>97.8%</td><td>98.7%</td><td>97.1%</td><td>-</td></tr><tr><td>dist(20)</td><td>98.9%</td><td>98.6%</td><td>98.4%</td><td>98.9%</td></tr><tr><td> $\underline{dist(50)}$ </td><td>99.7%</td><td>98.6%</td><td>99.0%</td><td>99.2%</td></tr><tr><td>ts(5)</td><td>92.2%</td><td>58.3%</td><td>36.0%</td><td>-</td></tr><tr><td>ts(10)</td><td>91.6%</td><td>63.2%</td><td>49.0%</td><td>-</td></tr><tr><td>ts(20)</td><td>92.4%</td><td>73.5%</td><td>60.0%</td><td>91.6%</td></tr><tr><td>ts(50)</td><td>91.7%</td><td>74.4%</td><td>62.0%</td><td>90.2%</td></tr><tr><td>fp(8)</td><td>96.2%</td><td>93.2%</td><td>95.9%</td><td>97.7%</td></tr><tr><td>fp(16)</td><td>96.7%</td><td>97.5%</td><td>97.5%</td><td>99.2%</td></tr><tr><td>fp(32)</td><td>95.4%</td><td>97.3%</td><td>97.2%</td><td>99.5%</td></tr><tr><td>sts()</td><td>96.2%</td><td>85.7%</td><td>93.4%</td><td>-</td></tr></table>

Table 13: Streaming or Not classification task.

<table><tr><td></td><td>RF</td><td>SVM</td><td>LR</td><td>DEEP</td></tr><tr><td>dist(5)</td><td>82.4%</td><td>75.2%</td><td>69.8%</td><td>-</td></tr><tr><td>dist(10)</td><td>84.1%</td><td>80.0%</td><td>79.1%</td><td>-</td></tr><tr><td>dist(20)</td><td>82.2%</td><td>79.5%</td><td>79.4%</td><td>82.1%</td></tr><tr><td>dist(50)</td><td>80.4%</td><td>77.8%</td><td>78.5%</td><td>79.9%</td></tr><tr><td>ts(5)</td><td>68.1%</td><td>62.1%</td><td>59.3%</td><td>-</td></tr><tr><td>ts(10)</td><td>69.4%</td><td>65.3%</td><td>64.3%</td><td>-</td></tr><tr><td>ts(20)</td><td>69.9%</td><td>65.1%</td><td>64.4%</td><td>63.5%</td></tr><tr><td>ts(50)</td><td>69.5%</td><td>62.6%</td><td>63.1%</td><td>65.1%</td></tr><tr><td>fp(8)</td><td>79.1%</td><td>76.9%</td><td>75.9%</td><td>80.7%</td></tr><tr><td>fp(16)</td><td>79.1%</td><td>77.1%</td><td>78.5%</td><td>82.6%</td></tr><tr><td>fp(32)</td><td>76.3%</td><td>74.5%</td><td>76.2%</td><td>84.2%</td></tr><tr><td>sts()</td><td>80.1%</td><td>64.9%</td><td>71.7%</td><td>-</td></tr></table>

Moreover, larger representations tend to achieve higher accuracy, this is due to the granularity of the representations which allows identifying intrinsic behaviors unnoticeable in smaller or more coarse representations<sup>7</sup>.

Finally, small LR classifiers tend to achieve a very low ac curacy compared to other classifiers. However, this gap is significantly narrowed for larger representations, where LR classifiers with larger representations achieve nearly equivalent results to those achieved by stronger DEEP classifiers.

## B.2 Models’ Deployment Considerations

In this section, we discuss the real-time deployment consideration of our classifiers. Particularly, we examine the memory requirements and the throughput of different representations and classifiers. First, we compare the memory required for storing all flow representations until classification. This is factored by the flow rate in the network, the collection time τ, and by the representation size. We note that the memory required for storing the parameters of most classifiers is negligible compared to the flow representations.

Table 14: Memory requirements for representation types (for the ISCX classification tasks), with τ = 15s and a flow rate of 1 million flows per second.

<table><tr><td></td><td>Repr. Size (B)</td><td>Approx. Required Memory (B)</td></tr><tr><td>dist(5)</td><td>20</td><td>300.0M</td></tr><tr><td>dist(10)</td><td>40</td><td>600.0M</td></tr><tr><td>dist(20)</td><td>80</td><td>1.2G</td></tr><tr><td>dist(50)</td><td>200</td><td>3.0G</td></tr><tr><td>ts(5)</td><td>30</td><td>450.0M</td></tr><tr><td>ts(10)</td><td>60</td><td>900.0M</td></tr><tr><td>ts(20)</td><td>120</td><td>1.8G</td></tr><tr><td>ts(50)</td><td>300</td><td>4.5G</td></tr><tr><td>fp(8)</td><td>128</td><td>1.9G</td></tr><tr><td>fp(16)</td><td>512</td><td>7.7G</td></tr><tr><td>fp(32)</td><td>2048</td><td>30.7G</td></tr><tr><td>sts()</td><td>132</td><td>2.0G</td></tr></table>

Table 14 shows an approximation of the total required memory for storing flow representations<sup>8</sup>. We can see that some representations (like larger dist and fp representations) may be impractical for real-time use on edge devices in a large network.

The second objective we explore is the throughput of the models. That is, the number of flows processed by a classifier within a specified timeframe, measured based on given computational capabilities. Specifically, we measured the number of flows classified within a 60-second period, using batches of 1000 samples. This method allows classifiers to perform batch operations more efficiently than single-sample classification (e.g. matrix multiplications).

Table 15 shows the throughput of different classifiers for different representations. It only includes the throughput calculated on models trained on the ISCX APPS classification task, however, as the required computational power merely changes across datasets or classification tasks, we observed similar results for the other tasks. The absolute numbers strongly depend on the deployment setting which in our case was an otherwise unloaded machine with an Intel core i7-1165G7 processor (@ 2.80GHz 1.69GHz) with 16GB RAM, using Python’s Keras for DEEP CNNs (with tensorflow CPU backend) and SKlearn for RF, LR, and SVM classifiers.

Table 15: Classification throughput (in flows per second, using batches of 1K representations) for the ISCX Applications classification task.

<table><tr><td></td><td>RF</td><td>SVM</td><td>LR</td><td>DEEP</td></tr><tr><td>dist(5)</td><td>96.3K</td><td>15.4K</td><td>7.7M</td><td>-</td></tr><tr><td>dist(10)</td><td>95.7K</td><td>13.8K</td><td>1.7M</td><td>-</td></tr><tr><td>dist(20)</td><td>93.7K</td><td>11.6K</td><td>1.4M</td><td>9.2K</td></tr><tr><td>dist(50)</td><td>89.2K</td><td>10.1K</td><td>894.2K</td><td>8.7K</td></tr><tr><td>ts(5)</td><td>95.5K</td><td>9.5K</td><td>7.4M</td><td>-</td></tr><tr><td>ts(10)</td><td>94.2K</td><td>9.4K</td><td>1.8M</td><td>-</td></tr><tr><td>ts(20)</td><td>91.0K</td><td>8.2K</td><td>1.4M</td><td>9.2K</td></tr><tr><td>ts(50)</td><td>84.9K</td><td>6.1K</td><td>937.1K</td><td>8.8K</td></tr><tr><td>sts()</td><td>94.2K</td><td>10.9K</td><td>1.8M</td><td>-</td></tr><tr><td>fp(8)</td><td>91.8K</td><td>10.1K</td><td>1.4M</td><td>9.0K</td></tr><tr><td>fp(16)</td><td>73.5K</td><td>3.5K</td><td>551.9K</td><td>7.8K</td></tr><tr><td>fp(32)</td><td>53.3K</td><td>766.7</td><td>177.6K</td><td>6.1K</td></tr></table>

We can see that despite the high accuracy achieved by DEEP CNN classifiers, the classification throughput may be impractical if deployed in a large ISP network with millions of new flows per second. On the other hand, we can see that as expected, LR classifiers outperform other classifiers in terms of throughput by an order of magnitude.