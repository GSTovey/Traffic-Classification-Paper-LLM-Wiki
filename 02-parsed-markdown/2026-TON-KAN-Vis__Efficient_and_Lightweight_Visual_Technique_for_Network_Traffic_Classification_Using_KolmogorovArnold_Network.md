# KAN-VIS: Eficient and Lightweight Visual Technique for Network Trafic Classification Using Kolmogorov–Arnold Network

Anurag Dutta , Graduate Student Member, IEEE, Pallavi Anand , Sangita Roy , Member, IEEE, and Rajat Subhra Chakraborty , Senior Member, IEEE

Abstract—Network trafic classification is a problem of fundamental importance in network security, and has been widely researched. However, the complexity of the problem has increased substantially in recent years, since most modern network trafic is encrypted end-to-end, and often further protected using VPN, and anonymization schemes like Tor. Existing methods have extracted important statistical features from the network trafic flow and used them to classify the trafic using machine learning. In this research, a set of four visual network trafic classifiers (KAN-VIS) based on the novel Kolmogorov-Arnold Network architecture is proposed. The input to these models will be a pictorial representation of the time series of packet-size histograms. The models were evaluated across five benchmark datasets. On ISCX datasets, KAN-VIS outperforms state-of-the-art techniques by 2.03%, 0.52%, and 1.98% for regular, Tor-encrypted, and VPN-protected trafic flows, respectively. KAN-VIS models also generalize for modern encryption protocols, where they achieve a 3.24% improvement over the best of existing ensemble models on CIC-IDS-2018 botnet detection, a 0.13% improvement over the state-of-the-art CNN on CESNET-QUIC22 with the IETF QUIC v1 protocol, and a 1.09% improvement on CipherSpectrum with TLS 1.3 for 40-class website fingerprinting.

Index Terms—Network forensics, network trafic classification, Kolmogorov-Arnold network.

## I. INTRODUCTION

N <sup>ETWORK</sup> <sup>trafic</sup> <sup>is</sup> <sup>the</sup> <sup>data</sup> <sup>that</sup> <sup>traverses</sup> <sup>the</sup> <sup>network</sup> at a given point in time. With the growing prevalence of extremely large-scale cyberattacks, real-time and accurate network trafic classification is a very important capability to have. Network trafic classification is also essential to achieve other objectives such as malware detection [1], rate monitoring [2], ensuring Quality of Service (QoS), etc. [3]. Traditionally, simpler schemes such as inspection of TCP/UCP headers in network packets to find the ports [4], [5], and further using them to classify network trafic were used; however, because of the increasing usage of dynamic ports [6], these schemes are often inefective. Packet content (payload) analysis through “deep packet inspection” [7] has been another alternative; however, these techniques are computationally expensive, and the invasion of privacy concerns have made these techniques dificult to adopt. Also, for the first two decades of the Internet, network trafic was primarily unencrypted, which made packet content analysis easier. However, currently an estimated 80- 95% of the global network trafic is encrypted [8], making it dificult to perform network trafic classification.

Widespread usage of Virtual Private Networks (VPNs) [17] and network anonymization techniques like The Onion Router (Tor) [18] is exacerbating the problem. Hence, recent research on network trafic classification have focused on the identification of alternative signatures based on the measurable characteristics of the network trafic. The recent literature on content-agnostic network packet classification is divided into three categories, (a) statistical feature-based; (b) sequencebased, and (c) visual representation-based.

The visual representation-based techniques are relatively less-explored, but are very efective for network trafic classification. Fig. 1 shows the visual representation for some selected trafic flows. The state-of-the-art in visual representation-based is the FlowPic [3], [15] technique and its variants [19], where a visual representation of traffic characteristics–“histogram” plots of normalized network packet arrival times (seconds) and packet sizes (bytes) —- are constructed and then input to deep neural network for potential feature extraction, followed by classification. The FlowPic class of techniques outperforms techniques of other classes by nearly 3.89% in accuracy. Fig. 2 presents comparative plots for diferent state-of-the-art network trafic classification models across diferent categories, to establish this point.

This paper proposes a set of four visual representationbased lightweight classification methods, collectively termed as KAN-VIS, for network packet classification. KAN-VIS generates a two-dimensional visual representation (histogram) of dimensions 64 × 64, followed by feature extraction, and finally classification using the Kolmogorov-Arnold Networks [20]. The four diferent models provide a spectrum of architectures, allowing practitioners to select configurations that balance accuracy requirements with available computational resources. The KAN-VIS models collectively outperform the state-of-the-art deep learning-based models by 1.51% for “inter-class” classification accuracy and 2.26% for “intra-class” classification accuracy. Here, inter-class classification distinguishes between fundamentally diferent trafic categories (e.g., VoIP vs. File Transfer vs. Video), where trafic patterns show substantial behavioural diferences. In contrast, intra-class classification discriminates between similar applications within the same category (e.g., Skype vs. Hangouts vs. Facebook within VoIP), where pattern variations are to detected despite high similarity in trafic characteristics.

![](images/81e7c0158efa602149cbddeaea02823532f602891de7564345d00304d1f6f590.jpg)

![](images/a6eb8b2405e47e1c2232d5ebc5439dd15c3e23b984379a451217036b64ec5021.jpg)

![](images/6afdec7650a84b5f8f9ce6440966ed74a2ffa7fec5a3e974d8852554a2d456ea.jpg)

<table><tr><td>Skype</td><td>Hangouts</td><td>Facebook</td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr></table>

Fig. 1. Selected examples of two-dimensional visual representation for network trafic (of VoIP class) from ISCX datasets. The first row of images are corresponding to regular trafic flow, and the next rows are for Torencrypted, and VPN-protected flows.

The rest of the paper is organized as follows. Section II briefly discusses state-of-the-art research across the three main categories of network trafic classification models, and highlights how KAN-VIS addresses the limitations of the best existing approaches. Section III provides the necessary preliminaries, including the architecture of Kolmogorov-Arnold Networks and the Flowpic method for the visual representation of network trafic. Section IV presents the proposed methodology—KAN-VIS—with theoretical discussions of parameter counts in Subsection IV-A. Following this, Section V details the experimental evaluation, from both the inter-class and intra-class classification, and contrasts the performance of the proposed models to that of state-of-the-art methods. Finally, Section VI concludes the work.

## II. RELATED WORKS

This section presents an overview of the state-of-the-art, and the contrasting features of the proposed methodology. Prior content-agnostic encrypted trafic classification methods can be segregated into three main categories, (a) statistical feature-based, (b) sequence-based, and (c) visual representation-based. Statistical methods mostly depends on hand-crafted or protocol-based features and using those features by classical classifiers, while sequence-based deep models learn from raw byte (or packet) sequences; although efective, these approaches have non-trivial preprocessing and feature design overhead leading to higher computational cost when deployed at scale.

As mentioned previously, another category is visual representation-based trafic classification. Since our contribution is also a visual representation-based pipeline, we focus more on visual approaches throughout the research, although for comparison methods from the other two categories have been consulted. Lim et al. pre-processed the network trace file (.pcap) to convert them to (gray-scale) images that can be readily adsorbed by computer vision techniques for classification based on inherent class-specific patterns [13]. For the classification, they employed CNN and Residual Network, of which the latter performs well for larger payloads (≥ 64 bytes in size). hang et al. extended the conceptualization by Lim et al. to three-channelled RGB images [14], and classifying them using a CNN. Evaluating on the ISCX VPN-nonVPN dataset, and a custom-collected dataset, 3D-CNN achieved good accuracy (≈ 95%). Overall, this technique remained the state-of-the-art, until a more robust image representation of network trafic–FlowPic [3], [15] emerged.

## A. Our Contributions

Although FlowPic achieved the best classification accuracy, it required relatively large images (1500 × 1500) to be input to the model, limiting it’s applicability to resourceconstrained environments. This paper extends the FlowPic algorithm, improving it’s accuracy, while at the same time being lightweight and adaptable (generalizable) as per requirements. Further, FlowPic was devised using CNN, which increases model complexity with increasing number of layers. This paper improves on these by proposing, and implementing a set of four comparatively shallow neural networks—KAN-VIS, but with improved performance (accuracy). Besides, the four models provide practitioners with multiple operating points to trade of accuracy against computational cost (e.g., parameter count and inference time), allowing many deployment options across a wider range of resource constraints than a single fixedarchitecture model. Table I summarizes the contributions and the distinction with FlowPic, and mini-FlowPic.

![](images/9383298384207e51ea14c33714166b4c82420bd405605892c5525012607bac29.jpg)  
(a) Statistical feature-based methods

![](images/fc2a2ef2200343171d745c4ce4a49d7ce2f16ad21f40bffa14660744f5005b8e.jpg)  
(b) Sequence-based methods

![](images/af9f9345f8818f735011c2568b46bced610ec986d9407c0edb1f9230c189c417.jpg)  
(c) Visual feature-based methods  
Fig. 2. Bar charts showing network trafic classification accuracies for selected “statistical” [9], “sequence-based” [10], [11], [12], and “visual” [3], [13], [14], [15] methods on the ISCXTOR-nonTOR, and ISCXVPN-nonVPN dataset [16] datasets. The plots shows that while all methods achieve competitive performance, “visual” feature-based techniques performs better. KAN-VIS is the technique proposed in this paper.

TABLE I  
COMPARATIVE ANALYSIS OF “ VISUAL ” NETWORK TRAFFIC CLASSI-FICATION METHODS: FLOWPIC [3], MINI-FLOWPIC [19], AND THE PROPOSED KAN-VIS APPROACH

<table><tr><td>Criterion</td><td>FLOWPIC [3]</td><td>MINI-FLOWPIC [19]</td><td>KAN-VIS</td></tr><tr><td>Network Data Dimensionality</td><td>1500 × 1500 (fixed on MTU)</td><td>32 × 32 and 64 × 64</td><td>Configurable according to MTU</td></tr><tr><td>Learning Mechanism</td><td>Supervised</td><td>Unsupervised</td><td>Supervised</td></tr><tr><td>Architectural Variants</td><td>Only one</td><td>Only one</td><td>Four</td></tr><tr><td>Classifier Family</td><td colspan="2">Convolution Neural Networks (CNNs)</td><td>Kolmogorov-Arnold Networks (KANs)</td></tr><tr><td>Performance (Accuracy)</td><td>Modest (avg. ≈ 0.8324)</td><td>Better (avg. ≈ 0.9195)</td><td>Best (avg. ≈ 0.9379)</td></tr><tr><td>Efficiency (#Param.)</td><td>6.28M (best reported)</td><td>Not reported</td><td>5.92M (best reported)</td></tr><tr><td>Inference Time (sec.)</td><td>≈ 4–7 sec.</td><td>Not reported</td><td>≈ 2–6 sec.</td></tr><tr><td>Traffic Types</td><td>Regular, Tor, VPN</td><td>Regular, VoIP, Video</td><td>Regular, Tor, VPN, Malicious</td></tr><tr><td>#Datasets Evaluated</td><td>ISCX (Tor, VPN)</td><td>UC-Davis QUIC ISCX (VoIP, Video)</td><td>ISCX (Tor, VPN)CIC-IDS-2018CESNET-QUIC22CipherSpectrum</td></tr><tr><td>Encryption Protocols</td><td>Legacy TLS Limited QUIC (~ 2016)</td><td>Legacy TLS Google QUIC (~ 2018)</td><td>TLS 1.3IETF QUIC v1 (~ 2022)</td></tr></table>

## III. PRELIMINARIES

This section describes the necessary preliminaries of the work–Kolmogorov-Arnold Network and FlowPic, which serve as the cornerstone for KAN-VIS.

## A. Kolmogorov-Arnold Network

Kolmogorov Arnold Network (KAN) was introduced in [20] to overcome the limitations of the existing Multi-layer Perceptrons (MLPs). MLPs decide the numerical values of the node weights using a fixed activation functions, whereas KAN updates the weights using trainable activation functions. Inheriting from the “Universal Approximation Theorem” [21], for MLPs any function $\begin{array} { r l r } { y } & { { } = } & { f [ x ] } \end{array}$ can be approximated as $\mathbf { y } = \sum a \left[ \dot { \pmb { \Omega } } \cdot \mathbf { x } + \pmb { \beta } \right]$ , where a[·] is the fixed activation function (e.g. ReLU, tanH, etc.), and $\left( \omega _ { i , j } \in \Omega , \beta _ { j } \in \beta \right)$ are the model weights, and bias respectively.

Contrary to that, inheriting from the “Kolmogorov-Arnold Representation Theorem” [22], the approximation (for KAN) can be made as, $\mathbf { y } = \sum \Phi \left\lceil \sum \phi \left[ \mathbf { x } \right] \right\rceil$ , where $\phi _ { i , j } \in \phi$ are the real-valued functions (trainable, specifically B-Splines [23]), and $\Phi _ { \ell } \in \Phi$ is the mapping (composition) function of $\ell ^ { \mathrm { { t h } } }$ layer. Further, the real-valued functions are defined as:

$$
\phi_ {i, j} \left[ x _ {i} \right] = \mu_ {i, j} ^ {(b)} \cdot \left(\frac {x _ {i}}{1 + e ^ {- x _ {i}}}\right) + \mu_ {i, j} ^ {(s)} \cdot \sum_ {k = 1} ^ {\mathcal {K}} \lambda_ {i, j, k} \cdot \mathcal {B} _ {k} \left[ x _ {i} \right]\tag{1}
$$

and the composition functions as:

$$
\Phi_ {\ell} = \left[ \begin{array}{c c c c} \phi_ {\ell , 1, 1} & \phi_ {\ell , 1, 2} & \dots & \phi_ {\ell , 1, \mathrm{L}} \\ \phi_ {\ell , 2, 1} & \phi_ {\ell , 2, 2} & \dots & \phi_ {\ell , 2, \mathrm{L}} \\ \vdots & \vdots & \ddots & \vdots \\ \phi_ {\ell , \mathrm{L}, 1} & \phi_ {\ell , \mathrm{L}, 2} & \dots & \phi_ {\ell , \mathrm{L}, \mathrm{L}} \end{array} \right]; \quad \phi_ {\ell , i, j} \equiv \phi_ {i, j}\tag{2}
$$

where, $\left( \mu _ { i , j } ^ { \left( b \right) } , \mu _ { i , j } ^ { \left( s \right) } \right)$ are the weights for the “biological” term (Swish [24]), and “spline” term $( \lambda _ { i , j , k }$ being the spline coefficients).

The following three properties of network trafic data justify our choice of using KAN backbone for trafic classification:

1) Network trafic data shows temporal non-stationarity; the patterns change with applications and protocols. MLPs sufer from catastrophic forgetting [25] that makes distributional shifts in the trafic dificult to model, but the trainable B-spline activations in KANs are more robust to the variations in encrypted trafic.

2) The histograms used for visualization of network trafic are sparse, and mostly localized (refer to Section III-B) which are best captured using the composition functions in KANs through learnable univariate functions. Traditional dense layers require larger number of parameters for correlating packet-size and timing than KAN layers as the activation functions in MLPs are global and cannot be updated dynamically.

3) The network flows contain both smooth session-level trends and sharp burst-level transitions. The B-spline basis in $\phi _ { i , j }$ represents piecewise smooth functions, which enables KAN to model trafic dynamics at different temporal scales all under the same framework.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Histogram Generation Algorithm
Require: n, T, and Π ▷T, Π are n-dim vectors
Ensure: H$_{i,i}$ ∈ H ▷H is the 2-D Histogram
1: function SESSIONPLOTTER(n, T, Π)
2: Initialize vectors T, Π with NULL entries.
3: for i = 0 to n - -1 do
4:    T$_{i}$ ← (T$_{i}$-T$_{0}$/T$_{n-1}$-T$_{0}$) · # MTU
5:    T$_{i}$ ← (Π$_{i}$-Π$_{0}$/Π$_{n-1}$-Π$_{0}$) · # MTU
6: end for
7: Initialize H(# MTU×# MTU) ← 0(# MTU×# MTU)
8: for j = 0 to n - -1 do
9:    H[Π$_{j}$], [T$_{j}$] ← H[Π$_{j}$], [T$_{j}$] + 1
10: end for
11: return H
12: end function
</div>

## B. FlowPic Histogram for Trafic Visualization

“FlowPic” [3] was one of the early contributions towards visual representation-based techniques for network trafic identification. Shapira et al. in their contribution devised a methodology to convert network trafic time series (continuous) data to their (discrete) visual representation, as histograms.

Algorithm 1 takes a sequential data stream consisting of standard network parameters in the form, {Application, Source IP, Source Port, Destination IP, Destination Port, Protocol, Starting Timestamp (in UTC format), Number of Packets (n), n tuples of packet arrival times relative to the starting time (T ), n tuples of packet sizes (in bytes)}, and then constructing a two-dimensional histogram representing the joint distribution of normalized packet arrival times and their sizes for a network session. Initially, the packet arrival times (T) and sizes (Π) are standardized to a predetermined resolution, as specified by the definition of # MTU. The normalized values (in the range [0 255]) are thereafter used to index into the 2D histogram H, incrementing the count at the respective pixel for each packet, hence facilitating the visualization of the spatial and temporal aspects of network trafic.

Shapira and Shavitt [3], [15] considered MTU = 1500, which was updated to 32, and 64 in their follow-up work, mini-FlowPic [19]. KAN-VIS is inspired by the performance boost achieved by mini-FlowPic (dimension $6 4 \times 6 4 )$ . The design choices have been further justified in Section IV-B.

## IV. PROPOSED METHODOLOGY: KAN-VIS

KAN-VIS is a collection of four deep learning models with varying degrees of architectural complexity and efectiveness. The reason behind choosing the KAN architecture over other more common MLP-based architectures are that the latter tends to “forget” (this phenomenon is known as catastrophic forgetting) the temporal patterns learned from a given training data set over the course of time, leading to poor decision boundaries being set [20]. Since it’s inception, KANs have been used in several cross-domain applications [1], [26], and have shown consistent improvement compared to state-of-theart alternative techniques in many cases. To the best of our knowledge, this is the first work on network flow-based pattern recognition using KAN.

The four proposed models under KAN-VIS are as follows, described in order of increasing architectural complexity.

1) KAN-Linear (KAN-L) (Fig. 3a): The input histogram $\mathcal { H } _ { 6 4 \times 6 4 }$ is transformed to the flattened list $\pmb { \mathcal { L } }$ using a permutation matrix, as ${ \mathcal { L } } \ = \ \mathbf { P } \times \sec \left[ { \mathcal { H } } \right]$ where, vec [·] is the column-major vectorization [27], $\mathrm { i . e . } ,$ vec $\begin{array} { r l r } { [ \mathcal { H } ] } & { { } = } & { \big [ \mathcal { H } _ { 0 , 0 } \mathcal { H } _ { 1 , 0 } \ \cdot \cdot \cdot \ \mathcal { H } _ { 6 3 , 0 } \mathcal { H } _ { 0 , 1 } \ \cdot \cdot \cdot \ \mathcal { H } _ { 6 3 , 6 3 } \big ] ^ { \mathrm { I } } . } \end{array}$ The Permutation Matrix (P) is defined as, $P _ { k , \ell } = { \left\{ \begin{array} { l l } { 1 } & { { \mathrm { i f ~ } } k = i \cdot n + j { \mathrm { ~ a n d ~ } } \ell = j \cdot n + i } \\ { 0 } & { { \mathrm { o t h e r w i s e } } } \end{array} \right. }$ with $i , j \in \{ 0 , . . . , 6 3 \}$ . Thus, the matrix P rearranges the elements of vec [H] to produce the row-major order [27]. Thus, the flattened list (of features) [28], $\begin{array} { r l r } { \mathcal { L } } & { = } & { \left[ \mathcal { H } _ { 0 , 0 } \ \mathcal { H } _ { 0 , 1 } \ \cdot \cdot \cdot \ \mathcal { H } _ { 0 , 6 3 } \ \mathcal { H } _ { 1 , 0 } \ \cdot \cdot \cdot \ \mathcal { H } _ { 6 3 , 6 3 } \right] ^ { \mathrm { T } } } \end{array}$ is given to the KAN layer as input which processes the 4096 dimensional vector, and generates logits, $\mathcal { L } _ { \mathrm { l o g i t s } } = \Phi _ { \mathrm { { L } } } \circ \Phi _ { \mathrm { { L } ^ { - 1 } } } \circ \cdots \circ \Phi _ { 1 } [ \mathcal { L } ^ { ( 0 ) } \equiv \mathcal { L }$ (base input) which are passed to Softmax layer for output mapping, where, $\pmb { \mathscr { L } } ^ { ( \ell ) } = \Phi _ { \ell } |  \sum _ { i , j } \phi _ { i , j } ^ { ( \ell ) } [ \pmb { \mathscr { L } } _ { i } ^ { ( \ell - 1 ) } ] | \in \mathbb { R } ^ { d _ { \ell } }$ is the output of layer \`. For this research, $\mathrm { ~ L ~ } \stackrel { \_ } { = } \mathrm { ~ 1 0 ~ }$ were considered.

2) KAN-Convolution (KAN-C) (Fig. 3b): It is an incremental model on KAN-L. Here, featured from the input histograms, $\mathcal { H } _ { 6 4 \times 6 4 \times 1 } ^ { ( 0 ) } \equiv \mathcal { H } _ { 6 4 \times 6 4 }$ is extracted using a sequence of two convolutional layers with same filter size (here, $3 \times 3 )$ with $\mathtt { p a d } = 1$ , and a default stride of one. The first convolutional layer expects a input of dimension one, and produces a feature map as $\mathcal { H } _ { 6 4 \times 6 4 \times 5 } ^ { ( 1 ) } = \mathbf { C o n v } 2 \mathbf { D } _ { ( 3 \times 3 ) } \left[ \mathcal { H } _ { 6 4 \times 6 4 \times 1 } ^ { ( 0 ) } \right]$ or $\mathcal { H } _ { 6 4 \times 6 4 \times 5 } ^ { ( 1 ) } = \sum _ { m = 0 } ^ { 3 } \sum _ { n = 0 } ^ { 3 } \bigg [ \mathcal { K } _ { m , n } \odot \mathcal { H } _ { i + 1 \cdot m , j + 1 \cdot n } ^ { ( 0 ) } \bigg ] .$ A max-pooling [29] layer (filter size of two) follows the stack which produced the map, $\mathcal { H } _ { \mathrm { p o o l e d } } ^ { ( 1 ) } = \mathrm { M a x P o o l 2 D } _ { ( 2 \times 2 ) } \left\lceil \mathcal { H } _ { 6 4 \times 6 4 \times 5 } ^ { ( 1 ) } \right\rceil \quad \in \quad \mathbb { R } ^ { 3 2 \times 3 2 \times 5 }$ Similarly, after the second filtration, $\mathcal { H } _ { 3 2 \times 3 2 \times 2 5 } ^ { ( 2 ) }$ ∈ $\mathbb { R } ^ { 3 2 \times 3 2 \times 2 5 }$ , and $\mathcal { H } _ { \mathrm { p o o l e d } } ^ { ( 2 ) } \in \mathbb { R } ^ { 1 6 \times 1 6 \times 2 5 }$ are produced. The highest level map $\mathcal { H } _ { \mathrm { p o o l e d } } ^ { ( 2 ) }$ is then flattened, similar to the operations in KAN-L [28], to generate logits, and further using them to produce the output mapping (passing through Softmax layer).

3) KAN-Convolution with Batch Normalization (KAN<sup>b</sup>- C) (Fig. 3c): It is an incremental model on KAN-C. The architectural viewpoint is exactly similar to its’ primitive, with added batch-normalization layer after each convolution filter. After the first layer of filtration, the feature map $\left( \mathcal { Z } ^ { \left( 1 \right) } \in \mathbb { R } ^ { 6 4 \times 6 4 \times 5 } \right)$ is batch normalized as, $\mathcal { Z } ^ { ( 1 ) } = \gamma ^ { ( 1 ) } \cdot \frac { \mathcal { H } _ { 6 4 \times 6 4 \times 5 } ^ { ( 1 ) } - \bar { \mu } ^ { ( 1 ) } } { \sqrt { \Sigma ^ { ( 1 ) ^ { 2 } } + \epsilon } } + \delta ^ { ( 1 ) } ,$ with added noise, $\epsilon \mathrm { ~  ~ { ~ \sim ~ } ~ } \mathcal { N } ( 0 , \mathbb { I } _ { 5 } )$ . Similarly, after the second layer of filtration, the normalized feature map $\left( \mathcal { Z } ^ { \left( 2 \right) } \in \mathbb { R } ^ { 3 2 \times 3 2 \times 2 5 } \right)$ becomes, $\mathcal { Z } ^ { ( 2 ) } = \gamma ^ { ( 2 ) } \cdot \frac { \mathcal { H } _ { 3 2 \times 3 2 \times 2 5 } ^ { ( 2 ) } - \mu ^ { ( 2 ) } } { \sqrt { \Sigma ^ { ( 2 ) ^ { 2 } } + \epsilon } } + \delta ^ { ( 2 ) } ,$ with noise

![](images/c8195367e2a387b3a9b8263542cb0810a84d95cd6113a095358fd6247b721c0f.jpg)  
Fig. 3. The proposed set of four deep learning model architectures under KAN-VIS.

4) Dual KAN-Convolution $( \mathbf { K A N } ^ { 2 } { \cdot } \mathbf { C } )$ (Fig. 3d): It is an improved version of KAN-C. Rather than passing the features through a single KAN layer, here it is passed through two KAN layers in succession, one that maps between 6400 to 256 values, and the other that maps between 256 values and the number of output classes. This multi-layer KAN structure enables the model to capture richer details.

KAN-VIS gets $6 4 \times 6 4$ histograms as input, represented as two-dimensional grayscale image, where the intensity of each pixel corresponds to the frequency of specific features and this setup captures uni-modal information $( n _ { \mathrm { i n p u t } } = 1 )$ . The first set of convolutional layers in KAN-VIS expects $n _ { \mathrm { i n } } = 1$ (inputdimension), $n _ { \mathrm { o u t } } ~ = ~ 5$ (output-dimension) to extract spatial features, aligning with up to five trafic classes (for intraclass classification). The next layer scales to 25 outputs, and MaxPool2D with $2 \times 2$ kernel (default choice for kernel size) downscales the features. The remaining parameters were initialized based on the foundational choices, and the final configuration was selected using $k = 5$ fold cross-validation on the ISCX training split. We selected the hyperparameter set with the best mean validation accuracy across folds, then retrained the model on the full ISCX training split before evaluating once on the held-out test partition, to ensure no test-set leakage. Please note that “lightweight” in KAN-VIS refers to (a) compact visual inputs $( 6 4 ~ \times ~ 6 4$ histograms) and (b) shallow feature extractors, and it does not imply that each of the four variant has identical computational cost. Instead, KAN-VIS provides a spectrum of variants where KAN-L and KAN-C target resource-constrained deployments, while $\mathrm { K A N ^ { B } - C }$ and $\mathrm { K A N } ^ { 2 } { \mathrm { - } } \mathbf { C }$ introduce additional normalization and KAN depth respectively to trade better computation for improved accuracy when resources are available.

## A. Parameter Count

The input to each of the models in the KAN-VIS stack is an input histogram (single channeled, $\mathcal { C } _ { 0 } = 1 )$ of dimension $6 4 \times 6 4$ . The KAN layer expects the input in the form of flattened tensors prior to being computed by the KAN-Layer which maps the dimensionality of the input tensors (flattened) to the number of classes being targeted for the classification. Each of the four models under KAN-VIS difer in their parameter count, as described below:

1) KAN-Linear, which lacks a feature extraction stage, and directly maps the input to the number of output classes (# classes), the total number of parameters can be expressed as: $\mathcal { O } \left( \underbrace { \mathrm { k n o t s } \times \sum _ { \ell = 1 } ^ { \mathrm { L } } d _ { \ell - 1 } \cdot d _ { \ell } } _ { \mathrm { w t s . } ~ \mathrm { ~ \small ~ ( ~ K A N ) ~ } } \right) +$ $\mathcal { O } \left( \underbrace { \sum _ { \ell = 1 } ^ { L } d _ { \ell } } _ { \mathrm { b i a s } } \right)$ , where knots refer to the number of trainable parameters per spline, $d _ { \ell }$ refer to the dimensionality of layer \`. Note that the dimensionality for the last KAN layer is $d _ { \mathrm { L } } = \# \subset \mathrm { l } \mathsf { a s s e s } )$

2) KAN-Convolution, have a dedicated feature extraction stage, followed by feature mapping. Here, the total number of parameters can be expressed as: O kernel<sub>1</sub> × C<sub>0</sub> × C<sub>1</sub> + O C<sub>1</sub> + wts. (CNN ) bias (CNN )

![](images/14fcc116b84569c639f1613425e5e1d19f5354fd2762b16015d53dcd02edbb9e.jpg)

$$
\begin{array}{l} \mathcal {O} \left(\underbrace {\text { kernel } _ {2} \times \mathcal {C} _ {1} \times \mathcal {C} _ {2}} _ {\text { wts.   (CNN } _ {2})}\right) + \mathcal {O} \left(\underbrace {\mathcal {C} _ {2}} _ {\text { bias   (CNN } _ {2})}\right) + \\ \mathcal {O} \left(\underbrace {\text { knots } \times \sum_ {\ell = 1} ^ {L} d _ {\ell - 1} \cdot d _ {\ell}} _ {\text { wts.   (KAN) }}\right) + \mathcal {O} \left(\underbrace {\sum_ {\ell = 1} ^ {L} d _ {\ell}} _ {\text { bias   (KAN) }}\right), \text { where } \end{array}
$$

$\{ { \mathcal C } _ { 1 } , { \dot { { \mathcal C } } } _ { 2 } \} ~ \equiv ~ \{ 5 , 2 5 \}$ are the output dimensions for each of the convolutional layers (of kernel size kernel<sub>1</sub>, and kernel respectively. Here, the dimensionality for the first KAN layer (after passing through two consecutive Conv2D, and MaxPool2D sequence) is $\begin{array} { r } { d _ { 0 } = \frac { 6 4 } { \gamma 2 } \times \frac { 6 4 } { \gamma 2 } \times \mathcal { C } _ { 2 } = 6 4 0 0 } \end{array}$

3) KAN-Convolution with Batch Normalization have additional $2 \cdot ( { \mathcal { C } } _ { 1 } + { \mathcal { C } } _ { 2 } )$ parameters (on top of KAN-Convolution) corresponding to scales and ofsets per channel (output) [30]. In practice, the parameter counts for KAN-Convolution with Batch Normalization, and its’ primitive does not vary much.

4) Dual KAN-Convolution have an additional KAN layer, which results in an increased parameter count. The total number of parameters can be expressed

$$
\begin{array}{l} \text {as:} \mathcal {O} \left(\underbrace {\operatorname{kernel} _ {1} \times \mathcal {C} _ {0} \times \mathcal {C} _ {1}} _ {\text {wts.} (\mathbf {C N N} _ {1})}\right) + \mathcal {O} \left(\underbrace {\mathcal {C} _ {1}} _ {\text {bias} (\mathbf {C N N} _ {1})}\right) + \\ \mathcal {O} \left(\underbrace {\operatorname{kernel} _ {2} \times \mathcal {C} _ {1} \times \mathcal {C} _ {2}} _ {\text {wts.} (\mathbf {C N N} _ {2})}\right) + \mathcal {O} \left(\underbrace {\mathcal {C} _ {2}} _ {\text {bias} (\mathbf {C N N} _ {2})}\right) + \\ \mathcal {O} \left(\underbrace {\operatorname{knots} _ {1} \times \sum_ {\ell = 1} ^ {\mathrm{L}} d _ {\ell - 1} ^ {(1)} \cdot d _ {\ell} ^ {(1)}} _ {\text {wts.} (\mathbf {K A N} _ {1})}\right) + \mathcal {O} \left(\underbrace {\sum_ {\ell = 1} ^ {\mathrm{L}} d _ {\ell} ^ {(1)}} _ {\text {bias} (\mathbf {K A N} _ {1})}\right) + \\ \mathcal {O} \left(\underbrace {\operatorname{knots} _ {2} \times \sum_ {\ell = 1} ^ {\mathrm{L}} d _ {\ell - 1} ^ {(2)} \cdot d _ {\ell} ^ {(2)}} _ {\text {wts.} (\mathbf {K A N} _ {2})}\right) + \mathcal {O} \left(\underbrace {\sum_ {\ell = 1} ^ {\mathrm{L}} d _ {\ell} ^ {(2)}} _ {\text {bias} (\mathbf {K A N} _ {2})}\right). \end{array}
$$

Here, $\{ d _ { 0 } ^ { ( 1 ) } , d _ { 0 } ^ { ( 2 ) } \} \quad \equiv \quad \{ 6 4 0 0 , 2 5 6 \}$ , and $\begin{array} { r l } { \{ d _ { \mathrm { L } } ^ { ( 1 ) } , d _ { \mathrm { L } } ^ { ( 2 ) } \} } & { { } \equiv } \end{array}$ {256 # classes} respectively.

## B. Design Choices

The KAN-VIS models involve two sets of design choices: (a) the histogram resolution and (b) the KAN hyperparameters.

We chose a 64 × 64-dimensional histogram to balance representational fidelity and computational cost. Prior works have shown that reducing the actual histogram representational resolution $( 1 5 0 0 \times 1 5 0 0 )$ to small grids $( 3 2 \times 3 2$ or $6 4 \times 6 4 )$ preserves classification performance, significantly reducing computation and memory footprint. This choice is particularly important for KAN-based classifiers because the KAN layers consume flattened histograms; therefore, the KAN input size grows quadratically with the histogram image dimensions. Consequently, increasing the dimensions inflates the KAN mapping cost substantially with diminishing returns on sparse histogram representations, whereas decreasing the dimensions increases quantization by merging distinct packet sizes (time bins) and reduces class separability. Since our primary objective was to make the classifier lightweight, we experimented with three diferent input resolutions $( 3 2 \times 3 2$ $6 4 \times 6 4$ , and $1 2 8 \times 1 2 8 )$ to determine for the choice. We used the existing ISCX datasets (on which prior works have benchmarked) for the ablation and computed the change in Accuracy-Parameter Count (AC-PC) ratio for each of the settings and found 64 × 64 histogram size to be most suitable for accuracy–complexity trade-of. Increasing the resolution from $6 4 \times 6 4$ to $1 2 8 \times 1 2 8$ increases the KAN input fourfold but achieves only marginal accuracy improvement (0.29%) while quadrupling the parameter count. Conversely, reducing the resolution to $3 2 \times 3 2$ reduces parameters by 4× but decreases accuracy by (2.39%). Although experimentally we found that $6 4 \times 6 4$ histograms are the optimal resolution, the histogram generation process (as described in Algorithm 1) can be adapted depending on MTU.

KAN hyperparameters control the numerical stability of the trainable spline activations; for instance, the grid size (number of knots), the spline order $r ,$ and regularization (or stability) terms. We set $\mathtt { g r i d - s i z e } = 1 0 , r = 3 , \epsilon _ { \mathrm { n o i s e } } = 1 0 ^ { - 2 } .$ and $\epsilon _ { \mathcal { G } } = 2 \times 1 0 ^ { - 2 }$ for all KAN-VIS variants; grid-size = 10 and cubic splines $\left( r \quad = \quad 3 \right)$ provide the necessary nonlinearity to model the smooth, piecewise structure of the learned activation functions, while the noise term <sub>noise</sub> regularizes and $\epsilon _ { \mathcal { G } }$ improves stability during training.

## V. EXPERIMENTAL RESULTS

This section presents the experimental details, dataset(s) used, their pre-processing standards, and the observed performance when compared to state-of-the-art (as discussed in Section II) models for network trafic classification.

## A. Experimental Setup

To validate the proposed set of four models under KAN-VIS and evaluate their generalizability, we conducted experiments on five diferent benchmark datasets:

1) ISCX TOR-nonTOR and ISCX VPN-nonVPN [16], which contain packets across five application categories (browsing, chat, file transfer, video, and audio) with three flow types: regular, Tor-encrypted, and VPNprotected trafic.

2) CIC-IDS-2018 [31], which is a widely used intrusion detection dataset containing both “benign” and “malicious” trafic (botnet attacks).

3) CESNET-QUIC22 [32], which is a recent dataset with IETF QUIC v1 protocol trafic across 102 fine-grained application classes, including streaming services, chat applications, social media, and communication tools.

4) CipherSpectrum [33], which is an encrypted website fingerprinting dataset containing TLS 1.3 trafic from 40 popular website classes

These datasets cover diferent encryption protocols (legacy TLS, TLS 1.3, IETF QUIC v1), trafic types (benign, malicious, and application-specific), and classification granularities. For each of these datasets, where packet capture files (ext: .pcap) were available, they were first converted to .tsv (tab separated) files, and then using the histogram generation algorithm, these .tsv (or .csv) files were parsed to the resultant .npy histograms. The Python implementation scripts for each of these conversions can be availed from [34].

TABLE II  
COMPARISON OF MODELS ON THE ISCXTOR-NONTOR, AND ISCXVPN-NONVPN DATASETS, BASED ON THEIR PERFORMANCE ON Inter − Class CLASSIFICATION. BOLD INDICATES THE BEST SCORE FROM KAN-VIS, AND UNDERLINE DENOTES THE BEST FROM S-O-T-A

<table><tr><td rowspan="2">Metrics\Model</td><td colspan="3">Sequence-based Methods</td><td colspan="3">Visual-based Methods</td><td colspan="4">KAN-based Models (proposed)</td></tr><tr><td>DP-CNN</td><td>BLJAN</td><td>MH-NET</td><td>2D-CNN</td><td>3D-CNN</td><td>FLOWPic</td><td>KAN-L</td><td>KAN-C</td><td> $KAN^B$ -C</td><td> $KAN^2$ -C</td></tr><tr><td colspan="11">“Regular”-type Traffic</td></tr><tr><td>Accuracy</td><td>0.7772 ± 0.03</td><td>0.5560 ± 0.07</td><td>0.9175 ± 0.02</td><td>0.6832 ± 0.05</td><td>0.6291 ± 0.06</td><td>0.8798 ± 0.02</td><td>0.8638 ± 0.04</td><td>0.9207 ± 0.02</td><td>0.9361 ± 0.01</td><td>0.9153 ± 0.02</td></tr><tr><td>F1-Score</td><td>0.7806 ± 0.04</td><td>0.5715 ± 0.08</td><td>0.9149 ± 0.02</td><td>0.6667 ± 0.05</td><td>0.6082 ± 0.07</td><td>0.8827 ± 0.03</td><td>0.8701 ± 0.03</td><td>0.9234 ± 0.02</td><td>0.9372 ± 0.01</td><td>0.9173 ± 0.02</td></tr><tr><td>TTTr (s)</td><td>120.63 ± 3.54</td><td>95.40 ± 2.87</td><td>360.77 ± 8.91</td><td>540.24 ± 12.45</td><td>1185.56 ± 31.22</td><td>630.30 ± 15.78</td><td>352.87 ± 9.03</td><td>762.53 ± 18.34</td><td>533.03 ± 11.92</td><td>1134.33 ± 27.65</td></tr><tr><td>TTTe (s)</td><td>1.40 ± 0.08</td><td>1.02 ± 0.05</td><td>2.31 ± 0.12</td><td>3.82 ± 0.19</td><td>6.86 ± 0.31</td><td>4.06 ± 0.21</td><td>2.18 ± 0.11</td><td>1.91 ± 0.09</td><td>2.43 ± 0.13</td><td>3.80 ± 0.18</td></tr><tr><td colspan="11">“Tor”-encrypted Traffic</td></tr><tr><td>Accuracy</td><td>0.6622 ± 0.05</td><td>0.7580 ± 0.04</td><td>0.9465 ± 0.01</td><td>0.3781 ± 0.09</td><td>0.7837 ± 0.04</td><td>0.6786 ± 0.06</td><td>0.8041 ± 0.03</td><td>0.9449 ± 0.01</td><td>0.8794 ± 0.03</td><td>0.9514 ± 0.01</td></tr><tr><td>F1-Score</td><td>0.6342 ± 0.06</td><td>0.7762 ± 0.04</td><td>0.9453 ± 0.01</td><td>0.3576 ± 0.10</td><td>0.7534 ± 0.05</td><td>0.6804 ± 0.06</td><td>0.8046 ± 0.04</td><td>0.9451 ± 0.01</td><td>0.8777 ± 0.03</td><td>0.9508 ± 0.01</td></tr><tr><td>TTTr (s)</td><td>126.84 ± 4.12</td><td>104.31 ± 3.45</td><td>374.00 ± 9.67</td><td>542.97 ± 13.21</td><td>1279.33 ± 34.56</td><td>573.40 ± 14.89</td><td>255.89 ± 7.23</td><td>491.57 ± 11.98</td><td>474.77 ± 10.54</td><td>1141.85 ± 28.91</td></tr><tr><td>TTTe (s)</td><td>1.52 ± 0.09</td><td>1.30 ± 0.07</td><td>2.05 ± 0.11</td><td>3.73 ± 0.18</td><td>7.06 ± 0.33</td><td>4.88 ± 0.24</td><td>2.97 ± 0.14</td><td>3.01 ± 0.15</td><td>2.52 ± 0.12</td><td>5.49 ± 0.27</td></tr><tr><td colspan="11">“VPN”-encrypted Traffic</td></tr><tr><td>Accuracy</td><td>0.9270 ± 0.02</td><td>0.8539 ± 0.03</td><td>0.9341 ± 0.02</td><td>0.2887 ± 0.11</td><td>0.8445 ± 0.04</td><td>0.9387 ± 0.01</td><td>0.7747 ± 0.04</td><td>0.9146 ± 0.02</td><td>0.9573 ± 0.01</td><td>0.9469 ± 0.01</td></tr><tr><td>F1-Score</td><td>0.9283 ± 0.02</td><td>0.7646 ± 0.05</td><td>0.9341 ± 0.02</td><td>0.2219 ± 0.12</td><td>0.8436 ± 0.04</td><td>0.9226 ± 0.02</td><td>0.7737 ± 0.05</td><td>0.9138 ± 0.02</td><td>0.9573 ± 0.01</td><td>0.9475 ± 0.01</td></tr><tr><td>TTTr (s)</td><td>139.04 ± 4.67</td><td>196.53 ± 6.12</td><td>391.02 ± 10.34</td><td>540.77 ± 14.02</td><td>1344.62 ± 37.89</td><td>525.75 ± 13.56</td><td>493.59 ± 12.21</td><td>1059.22 ± 26.78</td><td>763.00 ± 19.45</td><td>1547.89 ± 41.23</td></tr><tr><td>TTTe (s)</td><td>1.65 ± 0.09</td><td>1.93 ± 0.10</td><td>2.57 ± 0.13</td><td>3.80 ± 0.19</td><td>7.25 ± 0.35</td><td>4.23 ± 0.22</td><td>2.19 ± 0.11</td><td>1.98 ± 0.10</td><td>2.55 ± 0.13</td><td>5.89 ± 0.28</td></tr><tr><td>#Param. (M)</td><td>2.87</td><td>5.14</td><td>8.63</td><td>4.71</td><td>13.56</td><td>6.28</td><td>5.92</td><td>7.07</td><td>7.07</td><td>16.82</td></tr></table>

The models under KAN-VIS were implemented using the PyTorch (v. 2.4) framework, and the experiments were carried out on a system with 16 GiB main memory, an Intel(R) Core(TM) i7-1065G7 @1.30 GHz processor, and an NVIDIA GeForce MX330 Graphics Processing Unit with 2 GiB in-built memory. Besides, the experiments were conducted on dataset split into 80-20 traintest division, and each models were trained for 10 epochs. All reported results are averaged over five independent runs with diferent random seeds. Both the code and the pictorial dataset (used in this research) have been made available at [34] to enable reproduction of the experiments, as well as to enable further research on this topic.

## B. Data Pre-Processing

These comparative techniques include: Securitas-C 4.5, SVM, BAYES [9], Deep Packet (DP-CNN) [10], Byte-Label Joint Attention Network (BLJAN) [11], Multi-View Heterogeneous Network (MH-NET) [12], 2D-CNN [13], 3D-CNN [14], FlowPic [3], CNN-LSTM [37], Basic Recurrent Neural Networks (RNN), Gated Recurrent Unit (GRU), Long Short-Term Memory (LSTM), Convolutional Neural Networks CNN, Sparse Autoencoders (SAE) [38], Local outlier factor-CNN (LOF-CNN) [39], MULTI-CNN [40], CNN-LSTM with Northern Goshawk Optimization Algorithm (NGO-CNN-LSTM) [41], Flow Sequence Network (FS-NET) [42], Federated Convolutional Network (FCN) [43], Ensemble Techniques (ET), and Residual Networks (RESNET) [33]. Tables II and III presents the results of the “interclass”, and “intra-class” classification task respectively on the ISCX datasets (with regular, Tor-encrypted, and VPN-protected flows). Table IV shows the “inter-class” classification results for CSE-CIC-IDS-2018 dataset. Since the CIC-IDS dataset does not define subclasses, intra-class evaluation is not applicable. Tables V and VI presents the results of the “inter-class”, and “intra-class” classification respectively on the CESNET-QUIC22 dataset. Similar to CSE-CIC-IDS-2018, CipherSpectrum don’t define subclasses, thus only inter-class classification was performed, as shown in Table VII.

For training the models, the arrival time for each packet was normalized in the range [0 64], and 64 tuples consisting of {arrival time (normalized, in seconds), packet size (in bytes)} were chosen uniformly across the session. This was done for each flow within each sub-class (e.g. “chat”), each trafic class (e.g. “Skype”), for each of Tor, VPN and regular trafic. The produced dataset was augmented using two state-of-theart data synthetization techniques–Aug-Mix [35], and Mix-Up [36]. Data augmentation was inspired by the modus-operandi of mini-FlowPic, where random noise, horizontal flip, etc. and similar trivial augmentation techniques were used, which resulted in improved model generalizability.

## C. Evaluation Results

To evaluate the proposed set of four deep learning models under KAN-VIS, they are compared against state-of-theart machine learning baselines for Accuracy, F1 score, Training Time (TTTr), and Testing (inference) Time (TTTe).

Across all five benchmark datasets, KAN-VIS achieves competitive-to-superior performance against the best reported baselines in each setting. On ISCX inter-class (Table II), the best KAN-VIS variants achieve 93.61% (regular), 95.14% (Tor), and 95.73% (VPN), improving over the best baseline by 2.03%, 0.52%, and 1.98% respectively. On CSE-CIC-IDS-2018 binary botnet detection (Table IV), KAN<sup>B</sup>-C reaches 98.32% accuracy. On CESNET-QUIC22 inter-class (102 classes, Table V), KAN<sup>B</sup>-C achieves 98.47% accuracy, with a 0.13% gain over the best CNN baseline (98.34%), and for intra-class classification (Table VI), KAN-VIS improves chat, social-media, and communication by 0.69%, 1.25% and 0.68% respectively. However, for trafic classification within streaming-type flows, KAN-VIS underperforms its strongest baseline by 0.36%. Finally, on the most recent CipherSpectrum dataset, in inter-class classification (Table VII), KAN-C attains 94.89% accuracy, improving over baseline by 1.09%.

TABLE III  
COMPARISON OF MODELS ON THE ISCX NETWORK FLOW DATA EVALUATED Intra − Class. THE TOP-2 (ONE FROM PROPOSED, AND ANOTHER FROM S-O-T-A) RESULTS HAVE BEEN PRESENTED

<table><tr><td rowspan="2">Metrics\Model</td><td colspan="2">Chat-type Traffic (6 subclasses)</td><td colspan="2">File Transfer-type Traffic (4 subclasses)</td><td colspan="2">Video-type Traffic (5 subclasses)</td><td colspan="2">VoIP-type Traffic (3 subclasses)</td></tr><tr><td>C 4.5</td><td> $KAN^B-C$ </td><td>FLOWPIC</td><td>KAN-C</td><td>MH-NET</td><td>KAN-C</td><td>DP-CNN</td><td> $KAN^B-C$ </td></tr><tr><td colspan="9">“Regular”-type Traffic</td></tr><tr><td>Accuracy</td><td>0.9407 ± 0.02</td><td>0.9509 ± 0.01</td><td>1.0000 ± 0.00</td><td>1.0000 ± 0.00</td><td>0.9638 ± 0.02</td><td>0.9812 ± 0.01</td><td>0.9566 ± 0.02</td><td>1.0000 ± 0.00</td></tr><tr><td>F1-Score</td><td>0.9420 ± 0.02</td><td>0.9515 ± 0.01</td><td>1.0000 ± 0.00</td><td>1.0000 ± 0.00</td><td>0.9637 ± 0.02</td><td>0.9814 ± 0.01</td><td>0.9556 ± 0.02</td><td>1.0000 ± 0.00</td></tr><tr><td>TTTr (s)</td><td>9.21 ± 0.34</td><td>1130.90 ± 29.87</td><td>1720.25 ± 45.67</td><td>1289.54 ± 33.21</td><td>1505.87 ± 40.12</td><td>1544.94 ± 42.34</td><td>429.25 ± 11.78</td><td>1272.53 ± 35.89</td></tr><tr><td>TTTe (s)</td><td>0.06 ± 0.01</td><td>2.27 ± 0.11</td><td>5.27 ± 0.25</td><td>2.90 ± 0.14</td><td>3.90 ± 0.19</td><td>4.02 ± 0.20</td><td>1.22 ± 0.06</td><td>2.00 ± 0.10</td></tr><tr><td>#Param. (M)</td><td>0.05</td><td>8.05</td><td>9.80</td><td>8.19</td><td>9.53</td><td>8.95</td><td>2.93</td><td>8.01</td></tr></table>

<table><tr><td></td><td>C 4.5</td><td>KAN-C</td><td>MH-NET</td><td> $KAN^B-C$ </td><td>BLJAN</td><td> $KAN^B-C$ </td><td>SVM</td><td> $KAN^B-C$ </td></tr><tr><td>Accuracy</td><td>0.9554 ± 0.02</td><td>0.9786 ± 0.01</td><td>0.9798 ± 0.01</td><td>0.9966 ± 0.00</td><td>0.9962 ± 0.00</td><td>0.9997 ± 0.00</td><td>0.9292 ± 0.03</td><td>0.9573 ± 0.02</td></tr><tr><td>F1-Score</td><td>0.9556 ± 0.02</td><td>0.9787 ± 0.01</td><td>0.9798 ± 0.01</td><td>0.9965 ± 0.00</td><td>0.9963 ± 0.00</td><td>0.9997 ± 0.00</td><td>0.9288 ± 0.03</td><td>0.9573 ± 0.02</td></tr><tr><td>TTTr (s)</td><td>9.78 ± 0.38</td><td>1231.45 ± 32.54</td><td>1575.75 ± 41.89</td><td>1255.81 ± 33.67</td><td>135.79 ± 4.45</td><td>1229.42 ± 32.12</td><td>5.22 ± 0.21</td><td>1262.74 ± 34.01</td></tr><tr><td>TTTe (s)</td><td>0.02 ± 0.00</td><td>1.59 ± 0.08</td><td>2.97 ± 0.14</td><td>2.62 ± 0.13</td><td>0.89 ± 0.04</td><td>2.80 ± 0.14</td><td>0.24 ± 0.01</td><td>2.31 ± 0.11</td></tr><tr><td>#Param. (M)</td><td>0.03</td><td>8.15</td><td>9.73</td><td>8.37</td><td>5.27</td><td>7.96</td><td>0.11</td><td>8.00</td></tr></table>

<table><tr><td></td><td>FLOWPic</td><td>KAN2-C</td><td>MH-NET</td><td>KAN-C</td><td>3D-CNN</td><td>KAN-C</td><td>FLOWPic</td><td> $KAN^B-C$ </td></tr><tr><td>Accuracy</td><td>0.9312 ± 0.03</td><td>0.9649 ± 0.02</td><td>0.9466 ± 0.02</td><td>0.9938 ± 0.00</td><td>0.9997 ± 0.00</td><td>0.9997 ± 0.00</td><td>0.9452 ± 0.02</td><td>0.9791 ± 0.01</td></tr><tr><td>F1-Score</td><td>0.9311 ± 0.03</td><td>0.9648 ± 0.02</td><td>0.9466 ± 0.02</td><td>0.9938 ± 0.00</td><td>0.9997 ± 0.00</td><td>0.9997 ± 0.00</td><td>0.9452 ± 0.02</td><td>0.9791 ± 0.01</td></tr><tr><td>TTTr (s)</td><td>1769.65 ± 46.89</td><td>1267.73 ± 33.45</td><td>1631.77 ± 43.21</td><td>1080.63 ± 28.67</td><td>1409.53 ± 37.34</td><td>1195.02 ± 31.67</td><td>1751.61 ± 46.12</td><td>1314.65 ± 34.89</td></tr><tr><td>TTTe (s)</td><td>4.88 ± 0.24</td><td>2.73 ± 0.13</td><td>3.02 ± 0.15</td><td>3.51 ± 0.17</td><td>7.18 ± 0.35</td><td>3.67 ± 0.18</td><td>4.72 ± 0.23</td><td>2.98 ± 0.14</td></tr><tr><td>#Param. (M)</td><td>6.52</td><td>7.47</td><td>9.12</td><td>7.98</td><td>13.66</td><td>7.30</td><td>6.39</td><td>8.23</td></tr></table>

TABLE IV

COMPARISON OF MODELS ON THE CSE-CIC-IDS-2018 DATASET, BASED ON THEIR PERFORMANCE ON inter − class CLASSIFICATION (BOTNET). BOLD INDICATES THE BEST SCORE FROM KAN-VIS, AND UNDERLINE DENOTES THE BEST FROM S-O-T-A

<table><tr><td rowspan="2">Metrics\Model</td><td colspan="3">Sequence-based Methods</td><td colspan="3">Visual-based Methods</td><td colspan="4">KAN-based Models (proposed)</td></tr><tr><td>CNN-LSTM</td><td>LSTM</td><td>RNN</td><td>CNN</td><td>2D-CNN</td><td>LOF-CNN</td><td>KAN-L</td><td>KAN-C</td><td> $\text{KAN}^{\text{B}}\text{-C}$ </td><td> $\text{KAN}^{\text{2}}\text{-C}$ </td></tr><tr><td>Accuracy</td><td>0.9523 ± 0.02</td><td>0.7847 ± 0.03</td><td>0.8219 ± 0.04</td><td>0.8936 ± 0.03</td><td>0.7628 ± 0.04</td><td> $\underline{0.9987} \pm 0.00$ </td><td>0.9674 ± 0.01</td><td>0.9745 ± 0.01</td><td> $\textbf{0.9832} \pm 0.01$ </td><td>0.9796 ± 0.01</td></tr><tr><td>F1-Score</td><td>0.9418 ± 0.02</td><td>0.4453 ± 0.05</td><td>0.7865 ± 0.04</td><td>0.9234 ± 0.03</td><td>0.3587 ± 0.06</td><td> $\underline{0.9912} \pm 0.00$ </td><td>0.9628 ± 0.02</td><td>0.9701 ± 0.01</td><td> $\textbf{0.9809} \pm 0.01$ </td><td>0.9768 ± 0.01</td></tr><tr><td>TTTr (s)</td><td>247.38 ± 7.21</td><td>201.54 ± 5.93</td><td>213.72 ± 6.41</td><td>316.95 ± 9.51</td><td>426.83 ± 12.74</td><td>391.26 ± 11.34</td><td>282.67 ± 8.24</td><td>299.45 ± 8.98</td><td>314.58 ± 9.31</td><td>431.79 ± 12.56</td></tr><tr><td>TTTe (s)</td><td>2.89 ± 0.14</td><td>2.17 ± 0.11</td><td>2.38 ± 0.12</td><td>3.51 ± 0.18</td><td>5.74 ± 0.29</td><td>4.29 ± 0.21</td><td>2.73 ± 0.14</td><td>2.94 ± 0.15</td><td>3.18 ± 0.16</td><td>4.62 ± 0.23</td></tr><tr><td>#Param. (M)</td><td>3.45</td><td>2.87</td><td>2.15</td><td>4.21</td><td>4.71</td><td>5.89</td><td>5.92</td><td>7.07</td><td>7.07</td><td>16.82</td></tr></table>

TABLE V

COMPARISON OF MODELS ON THE CESNET-QUIC22 DATASET, BASED ON THEIR PERFORMANCE ON inter − class CLASSIFICATION (102 APPLICATION CLASSES). BOLD INDICATES THE BEST SCORE FROM KAN-VIS, AND UNDERLINE DENOTES THE BEST FROM S-O-T-A

<table><tr><td rowspan="2">Metrics\Model</td><td colspan="3">Sequence-based Methods</td><td colspan="3">Visual-based Methods</td><td colspan="4">KAN-based Models (proposed)</td></tr><tr><td>LSTM</td><td>GRU</td><td>NG-C-LSTM</td><td>CNN</td><td>MULTI-CNN</td><td>SAE</td><td>KAN-L</td><td>KAN-C</td><td> $\text{KAN}^{\text{B}}\text{-C}$ </td><td> $\text{KAN}^{\text{2}}\text{-C}$ </td></tr><tr><td>Accuracy</td><td>0.9412 ± 0.02</td><td>0.9328 ± 0.02</td><td>0.9527 ± 0.01</td><td>0.9834 ± 0.00</td><td>0.9055 ± 0.02</td><td>0.8956 ± 0.03</td><td>0.9683 ± 0.01</td><td>0.9756 ± 0.01</td><td>0.9847 ± 0.01</td><td>0.9812 ± 0.01</td></tr><tr><td>F1-Score</td><td>0.9387 ± 0.02</td><td>0.9301 ± 0.02</td><td>0.9520 ± 0.01</td><td>0.9812 ± 0.00</td><td>0.9034 ± 0.02</td><td>0.8923 ± 0.03</td><td>0.9658 ± 0.01</td><td>0.9729 ± 0.01</td><td>0.9823 ± 0.01</td><td>0.9789 ± 0.01</td></tr><tr><td>TTTr (s)</td><td>358.47 ± 10.45</td><td>342.19 ± 9.87</td><td>423.56 ± 12.34</td><td>289.73 ± 8.56</td><td>412.85 ± 11.98</td><td>267.92 ± 7.89</td><td>395.28 ± 11.23</td><td>418.64 ± 12.01</td><td>437.91 ± 12.67</td><td>562.45 ± 16.34</td></tr><tr><td>TTTe (s)</td><td>3.76 ± 0.18</td><td>3.58 ± 0.17</td><td>4.45 ± 0.22</td><td>3.12 ± 0.15</td><td>4.89 ± 0.24</td><td>2.87 ± 0.14</td><td>3.94 ± 0.19</td><td>4.23 ± 0.21</td><td>4.51 ± 0.22</td><td>5.87 ± 0.29</td></tr><tr><td>#Param. (M)</td><td>3.12</td><td>2.98</td><td>4.56</td><td>5.23</td><td>6.45</td><td>4.87</td><td>6.21</td><td>7.89</td><td>7.89</td><td>18.45</td></tr></table>

TABLE VI  
COMPARISON OF MODELS ON THE CESNET-QUIC22 NETWORK FLOW DATA EVALUATED Intra − Class. THE TOP-2 (ONE FROM PROPOSED, AND ANOTHER FROM S-O-T-A) RESULTS HAVE BEEN PRESENTED

<table><tr><td rowspan="2">Metrics\Model</td><td colspan="2">Streaming-type Traffic (15 subclasses)</td><td colspan="2">Chat-type Traffic (8 subclasses)</td><td colspan="2">Social Media-type Traffic (6 subclasses)</td><td colspan="2">Communication-type Traffic (9 subclasses)</td></tr><tr><td>FCN</td><td>KAN-C</td><td>FCN</td><td> $\text{KAN}^{\text{B}}\text{-C}$ </td><td>FCN</td><td>KAN-C</td><td>CNN</td><td> $\text{KAN}^{\text{B}}\text{-C}$ </td></tr><tr><td>Accuracy</td><td>0.9912 ± 0.01</td><td>0.9876 ± 0.01</td><td>0.9734 ± 0.01</td><td>0.9801 ± 0.01</td><td>0.9526 ± 0.02</td><td>0.9645 ± 0.01</td><td>0.9845 ± 0.01</td><td>0.9912 ± 0.01</td></tr><tr><td>F1-Score</td><td>0.9908 ± 0.01</td><td>0.9867 ± 0.01</td><td>0.9718 ± 0.01</td><td>0.9789 ± 0.01</td><td>0.9508 ± 0.02</td><td>0.9623 ± 0.01</td><td>0.9834 ± 0.01</td><td>0.9901 ± 0.01</td></tr><tr><td>TTTr (s)</td><td>156.43 ± 4.67</td><td>412.78 ± 12.34</td><td>178.92 ± 5.34</td><td>438.56 ± 13.12</td><td>143.67 ± 4.21</td><td>395.24 ± 11.78</td><td>289.35 ± 8.67</td><td>456.89 ± 13.67</td></tr><tr><td>TTTe (s)</td><td>1.67 ± 0.08</td><td>4.23 ± 0.21</td><td>1.89 ± 0.09</td><td>4.51 ± 0.22</td><td>1.52 ± 0.08</td><td>4.06 ± 0.20</td><td>3.12 ± 0.15</td><td>4.68 ± 0.23</td></tr><tr><td>#Param. (M)</td><td>2.34</td><td>7.89</td><td>2.34</td><td>7.89</td><td>2.34</td><td>7.89</td><td>5.23</td><td>7.89</td></tr></table>

Table VIII gives the ablation study for diferent computational layers in KAN-VIS models, and Fig. 4 presents the confusion matrices for the proposed KAN-VIS models, and the baseline FlowPic model respectively. Since the FlowPic paper reports the confusion matrices corresponding to ISCX datasets only, we restricted our matrices to that dataset. As evident from Table VIII, adding more than two KAN layers improves validation accuracy, but increases inference time beyond baseline. The reason behind choosing a FFNN + Conv2D Block as the baseline is that it represents a standard

TABLE VII  
COMPARISON OF MODELS ON THE CIPHERSPECTRUM DATASET, BASED ON THEIR PERFORMANCE ON Inter − Class CLASSIFICATION (40 WEBSITE CLASSES). BOLD INDICATES THE BEST SCORE FROM KAN-VIS, AND UNDERLINE DENOTES THE BEST FROM S-O-T-A

<table><tr><td rowspan="2">Metrics\Model</td><td colspan="3">Sequence-based Methods</td><td colspan="3">Visual-based Methods</td><td colspan="4">KAN-based Models (proposed)</td></tr><tr><td>LSTM</td><td>FS-NET</td><td>ET</td><td>1D-CNN</td><td>2D-CNN</td><td>1D-RESNET</td><td>KAN-L</td><td>KAN-C</td><td> $\text{KAN}^{\text{B}}\text{-C}$ </td><td> $\text{KAN}^{\text{2}}\text{-C}$ </td></tr><tr><td>Accuracy</td><td>0.8534 ± 0.03</td><td>0.9125 ± 0.02</td><td>0.9387 ± 0.01</td><td>0.8967 ± 0.02</td><td>0.9234 ± 0.02</td><td>0.9312 ± 0.01</td><td>0.9156 ± 0.02</td><td>0.9489 ± 0.01</td><td>0.9423 ± 0.01</td><td>0.9378 ± 0.01</td></tr><tr><td>F1-Score</td><td>0.8489 ± 0.03</td><td>0.9098 ± 0.02</td><td>0.9365 ± 0.01</td><td>0.8934 ± 0.02</td><td>0.9212 ± 0.02</td><td>0.9289 ± 0.01</td><td>0.9123 ± 0.02</td><td>0.9467 ± 0.01</td><td>0.9401 ± 0.01</td><td>0.9356 ± 0.01</td></tr><tr><td>TTTr (s)</td><td>423.56 ± 12.67</td><td>356.78 ± 10.45</td><td>189.23 ± 5.67</td><td>398.45 ± 11.89</td><td>512.67 ± 15.34</td><td>467.89 ± 13.98</td><td>378.92 ± 11.12</td><td>401.56 ± 12.01</td><td>423.78 ± 12.67</td><td>541.23 ± 16.23</td></tr><tr><td>TTTe (s)</td><td>4.45 ± 0.22</td><td>3.78 ± 0.19</td><td>2.01 ± 0.10</td><td>4.12 ± 0.20</td><td>5.34 ± 0.26</td><td>4.89 ± 0.24</td><td>3.98 ± 0.19</td><td>4.23 ± 0.21</td><td>4.45 ± 0.22</td><td>5.67 ± 0.28</td></tr><tr><td>#Param. (M)</td><td>3.89</td><td>4.56</td><td>2.12</td><td>5.67</td><td>6.23</td><td>7.45</td><td>6.78</td><td>8.12</td><td>8.12</td><td>19.34</td></tr></table>

![](images/08f8b8fc7a18c00b0b63379415787bdfb88299cdb5459b33f67b0781f5135453.jpg)

![](images/f0191b7dbd6b2671c91fa6d3e418883f752ae0c21362d65b17207fa3393caeef.jpg)

![](images/1048a6abc8ebcfbac505daa69025ea954d2a6bf192a78e9110c150bd1fbcc6af.jpg)  
(b) Tor-enc. Flow  
(c) VPN-prot. Flow

(a) Regular Flow  
Matrices for (selective best from) KAN-VIS models  
![](images/690044e8092ad882db2bdc30d107fa9bc497497b0b606ddc6ffd499fcabcb7d8.jpg)  
(a) Regular Flow

![](images/4559deb49a6e5c7eb23af3952eb3d09b25480c257ce5dcdce579e3edd0d32f23.jpg)  
(b) Tor-enc. Flow

![](images/c4cc0b4fc916fd5abd451ab71729690b18d5b51eb0e3a9402ae4568a4741b4fd.jpg)  
(c) VPN-prot. Flow  
Matrices for Baseline, as reported in FlowPic [3] [15]  
Fig. 4. Confusion matrices for the visual-network trafic classification models.

CNN architecture with fixed activations (ReLU), which makes it easier to identify the contribution of KAN’s trainable B-spline activations. The table also validates the choice of two KAN layers in the model stack. The study additionally facilitates a spectrum of choice for the practitioner, enabling them to choose from the set of four models under KAN-VIS. Also, if the need is to classify trafic in a resource constrained environment, one can choose between KAN-Linear, and KAN-Convolution. Whereas if the classification can be supported by substantial hardware resources, high-end models like KAN-Convolution with Batch Normalization, and Dual KAN-Convolution can be used. Further, in the confusion matrices, KAN-VIS models show strong diagonal dominance with minimal of-diagonal confusion. For regular flows, most classes achieve more than 90% recall, with only minor overlaps between “Browsing” and “Files” (i.e., 7.8% overlap); for Tor-encrypted flows, all classes sustain more than 85% recall despite anonymization padding; and for VPNprotected flows, more-accurate classification with more than 94% recall is achieved across all categories. In contrast, FlowPic sufers severe false predictions, especially for Torencrypted trafic, where “Files” are misclassified as “VoIP”

TABLE VIII  
IMPLICATIONS OF DIFFERENT COMPUTATIONAL LAYERS FOR THE CLASSIFICATION PROCESS

<table><tr><td colspan="2">Layer specific Update(particular to classification)</td><td colspan="4">Initial Observational Metrics(old configuration)</td><td colspan="4">Post-update Observational Metrics(updated configuration)</td></tr><tr><td>Old Configuration</td><td>New Configuration</td><td>Accuracy(stdev.)</td><td>TTTr(sec.)</td><td>TTTe(sec.)</td><td>Model Size(#Param.)</td><td>Accuracy(stdev)</td><td>TTTr(sec.)</td><td>TTTe(sec.)</td><td>Model Size(#Param.)</td></tr><tr><td>Feed-Forward NN (×1)</td><td>Feed-Forward NN (×2)</td><td>0.8221(0.0017)</td><td>3.18</td><td>0.05</td><td>0.09</td><td>0.8485(0.0013)</td><td>9.40</td><td>1.22</td><td>0.27</td></tr><tr><td>Feed-Forward NN (×2)</td><td>Feed-Forward NN (×3)</td><td>0.8485(0.0013)</td><td>9.40</td><td>1.22</td><td>0.27</td><td>0.8460(0.0014)</td><td>17.62</td><td>4.00</td><td>0.65</td></tr><tr><td>Feed-Forward NN (×2)</td><td>Feed-Forward NN+ Convolution Block</td><td>0.8485(0.0013)</td><td>9.40</td><td>1.22</td><td>0.27</td><td>0.8951(0.0027)</td><td>101.69</td><td>2.49</td><td>1.90</td></tr><tr><td>Feed-Forward NN+ Convolution Block</td><td>Feed-Forward NN (×2)+ Convolution Block</td><td>0.8951(0.0027)</td><td>101.69</td><td>2.49</td><td>1.90</td><td>0.8879(0.0015)</td><td>183.78</td><td>2.94</td><td>2.16</td></tr><tr><td>Feed-Forward NN (×2)+ Convolution Block</td><td>Feed-Forward NN+ Convolution Block (×2)</td><td>0.8879(0.0015)</td><td>183.78</td><td>2.94</td><td>2.16</td><td>0.9184(0.0018)</td><td>461.02</td><td>4.26</td><td>3.81</td></tr><tr><td colspan="2">Feed-Forward NN+ Convolution Block (×2)</td><td colspan="8">Baseline Model [3]</td></tr><tr><td>Feed-Forward NN+ Convolution Block (×2)</td><td>Convolution Block (×3)</td><td>0.9184(0.0018)</td><td>461.02</td><td>4.26</td><td>3.81</td><td>0.9207(0.0030)</td><td>709.86</td><td>6.47</td><td>6.20</td></tr><tr><td>KAN-Linear (×1)</td><td>KAN-Linear (×2)</td><td>0.9306(0.0009)</td><td>308.91</td><td>2.23</td><td>5.92</td><td>0.9339(0.0010)</td><td>416.53</td><td>4.01</td><td>6.16</td></tr><tr><td>KAN-Linear (×2)</td><td>KAN-Linear+ Convolution Block (×2)</td><td>0.9339(0.0010)</td><td>416.53</td><td>4.01</td><td>6.16</td><td>0.9519(0.0017)</td><td>735.64</td><td>6.49</td><td>7.07</td></tr><tr><td>KAN-Linear+ Convolution Block (×2)</td><td>KAN-Linear (×2)+ Convolution Block (×2)</td><td>0.9519(0.0017)</td><td>735.64</td><td>6.49</td><td>7.07</td><td>0.9786(0.0012)</td><td>1096.41</td><td>13.01</td><td>16.82</td></tr><tr><td>KAN-Linear (×2)+ Convolution Block (×2)</td><td>KAN-Linear (×3)+ Convolution Block (×2)</td><td>0.9786(0.0012)</td><td>1096.41</td><td>13.01</td><td>16.82</td><td>0.9705(0.0021)</td><td>2100.18</td><td>25.35</td><td>30.33</td></tr></table>

in 70.8% of cases, “Browsing” as “Chat” in 61.9% of cases, and also notably “Video” achieves only 43.2% recall with significant cross-class confusion.

These observations suggest that the large 1500 × 1500 histograms under FlowPic capture fine-grained features, but those become insuficient under strong circuit multiplexing (as done in Tor). Overall, KAN-VIS produces fewer false predictions, maintaining balanced class-wise performance across all trafic categories.

## VI. CONCLUSION

In this paper, KAN-VIS–an eficient and computationally lightweight visual-representation-based method for classification of network trafic has been introduced. The proposed technique is non-invasive, and works well for both regular, Tor-encrypted, and VPN network trafic. KAN-VIS outperforms several state-of-the-art network trafic classification techniques when applied to benchmark network trafic datasets. Future research can be directed towards application of the proposed models to other problems of network and systems security.

## REFERENCES

[1] A. Dutta, S. Prakash Nayak, R. Naskar, and R. S. Chakraborty, “Kol-4-gen: Stacked Kolmogorov–Arnold and generative adversarial networks for malware binary classification through visual analysis,” IEEE Embedded Syst. Lett., vol. 17, no. 4, pp. 268–271, Aug. 2025.

[2] A. D’Alconzo, I. Drago, A. Morichetta, M. Mellia, and P. Casas, “A survey on big data for network trafic monitoring and analysis,” IEEE Trans. Netw. Service Manage., vol. 16, no. 3, pp. 800–813, Sep. 2019.

[3] T. Shapira and Y. Shavitt, “FlowPic: A generic representation for encrypted trafic classification and applications identification,” IEEE Trans. Netw. Service Manage., vol. 18, no. 2, pp. 1218–1232, Jun. 2021.

[4] V. Ponnusamy, A. Yichiet, N. Jhanjhi, M. Humayun, and M. Fahhad Almufareh, “IoT wireless intrusion detection and network trafic analysis,” Comput. Syst. Sci. Eng., vol. 40, no. 3, pp. 865–879, 2022.

[5] W. Abduladheem Kamil, S. Awang Nor, and R. Alubady, “Performance evaluation of TCP, UDP and DCCP trafic over 4G network,” Res. J. Appl. Sci., Eng. Technol., vol. 11, no. 10, pp. 1048–1057, Dec. 2015.

[6] S. W. O’Malley and L. L. Peterson, “A dynamic network architecture,” ACM Trans. Comput. Syst., vol. 10, no. 2, pp. 110–143, 1992.

[7] R. T. El-Maghraby, N. M. Abd Elazim, and A. M. Bahaa-Eldin, “A survey on deep packet inspection,” in Proc. 12th Int. Conf. Comput. Eng. Syst. (ICCES), Dec. 2017, pp. 188–197.

[8] A. Hancock. The Last Mile of Encrypting the Web: 2023 Year in Review. Accessed: Oct. 2024. [Online]. Available: https://www.ef.org/deeplinks/ 2023/12/year-review-last-mile-encrypting-web

[9] X. Yun, Y. Wang, Y. Zhang, and Y. Zhou, “A semantics-aware approach to the automated network protocol identification,” IEEE/ACM Trans. Netw., vol. 24, no. 1, pp. 583–595, Feb. 2016.

[10] M. Lotfollahi, M. J. Siavoshani, R. S. H. Zade, and M. Saberian, “Deep packet: A novel approach for encrypted trafic classification using deep learning,” Soft Comput., vol. 24, no. 3, pp. 1999–2012, Feb. 2020.

[11] K. Mao, X. Xiao, G. Hu, X. Luo, B. Zhang, and S. Xia, “Byte-label joint attention learning for packet-grained network trafic classification,” in Proc. IEEE/ACM 29th Int. Symp. Quality Service (IWQOS), Jun. 2021, pp. 1–10.

[12] H. Zhang et al., “Revolutionizing encrypted trafic classification with MH-Net: A multi-view heterogeneous graph model,” in Proc. AAAI Conf. Artif. Intell., 2025, vol. 39, no. 1, pp. 1048–1056.

[13] H.-K. Lim, J.-B. Kim, J.-S. Heo, K. Kim, Y.-G. Hong, and Y.-H. Han, “Packet-based network trafic classification using deep learning,” in Proc. Int. Conf. Artif. Intell. Inf. Commun. (ICAIIC), Feb. 2019, pp. 046–051.

[14] J. Zhang, F. Li, F. Ye, and H. Wu, “Autonomous unknown-application filtering and labeling for DL-based trafic classifier update,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Jul. 2020, pp. 397–405.

[15] T. Shapira and Y. Shavitt, “FlowPic: Encrypted internet trafic classification is as easy as image recognition,” in Proc. IEEE Conf. Comput. Commun. Workshops (INFOCOM WKSHPS), Apr. 2019, pp. 680–687.

[16] A. H. Lashkari, G. D. Gil, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of Tor trafic using time-based features,” in Proc. 3rd Int. Conf. Inf. Syst. Secur. Privacy (ICISSP), Porto, Portugal, Feb. 2017, pp. 253–262.

[17] R. Venkateswaran, “Virtual private networks,” IEEE Potentials, vol. 20, no. 1, pp. 11–15, Feb./Mar. 2001.

[18] D. Goldschlag, M. Reed, and P. Syverson, “Onion routing,” Commun. ACM, vol. 42, no. 2, pp. 39–41, 1999.

[19] E. Horowicz, T. Shapira, and Y. Shavitt, “A few shots trafic classification with mini-FlowPic augmentations,” in Proc. 22nd ACM Internet Meas. Conf., 2022, pp. 647–654.

[20] Z. Liu et al., “KAN: Kolmogorov–Arnold networks,” 2024, arXiv:2404.19756.

[21] M. T. Augustine, “A survey on universal approximation theorems,” 2024, arXiv:2407.12895.

[22] J. Schmidt-Hieber, “The Kolmogorov–Arnold representation theorem revisited,” Neural Netw., vol. 137, pp. 119–126, May 2021.

[23] A. Pal and D. Das, “Understanding the limitations of B-spline KANs: Convergence dynamics and computational eficiency,” in Proc. NeurIPS Workshop Sci. Methods Understand. Deep Learn., 2024, pp. 1–7.

[24] P. Ramachandran, B. Zoph, and Q. V. Le, “Searching for activation functions,” 2017, arXiv:1710.05941.

[25] R. Kemker, M. McClure, A. Abitino, T. Hayes, and C. Kanan, “Measuring catastrophic forgetting in neural networks,” in Proc. AAAI Conf. Artif. Intell., 2018, vol. 32, no. 1, pp. 1–9.

[26] S. Somvanshi, S. A. Javed, M. M. Islam, D. Pandit, and S. Das, “A survey on Kolmogorov–Arnold network,” ACM Comput. Surv., vol. 58, no. 2, pp. 1–35, 2024.

[27] E. D. Cui, Vectorization: A Practical Guide to Eficient Implementations Mach. Learn. Algorithms. Hoboken, NJ, USA: Wiley, 2024.

[28] C. Chiu, A. Delanovic, J. Platts, A. Loy, and A. Beckus, “A methodology for flattening the command and control problem space,” in Artificial Intelligence and Machine Learning for Multi-Domain Operations Applications IV, vol. 12113. Bellingham, WA, USA: SPIE, 2022, pp. 253–265.

[29] H. Wu and X. Gu, “Max-pooling dropout for regularization of convolutional neural networks,” in Proc. 22nd Int. Conf. Neural Inf. Process. (ICONIP), Istanbul, Turkey. Cham, Switzerland: Springer, 2015, pp. 46–54.

[30] N. Bjorck, C. P. Gomes, B. Selman, and K. Q. Weinberger, “Understanding batch normalization,” in Proc. Adv. Neural Inf. Process. Syst., vol. 31, 2018, pp. 1–12.

[31] CSE-CIC-IDS2018 on AWS. Canadian Institutefor Cybersecurity (CIC), University of New Brunswick. Accessed: Feb. 14, 2026. [Online]. Available: https://www.unb.ca/cic/datasets/ids-2018.html

[32] J. Luxemburk, K. Hynek, T. Cejka, A. Luka<sup>ˇ</sup> coviˇ c, and P.ˇ Si<sup>ˇ</sup> ska,ˇ “CESNET-QUIC22: A large one-month QUIC network trafic dataset from backbone lines,” Data Brief, vol. 46, Feb. 2023, Art. no. 108888.

[33] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “SoK: Decoding the enigma of encrypted network trafic classifiers,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2025, pp. 1825–1843.

[34] A. Dutta, P. Anand, S. Roy, and R. S. Chakraborty. KAN-Vis: Eficient and Lightweight Visual Technique for Network Trafic Classification using Kolmogorov–Arnold Network. Accessed: Nov. 2024. [Online]. Available: https://github.com/Anurag-Dutta/KAN-Vis

[35] D. Hendrycks, N. Mu, E. D. Cubuk, B. Zoph, J. Gilmer, and B. Lakshminarayanan, “AugMix: A simple data processing method to improve robustness and uncertainty,” 2019, arXiv:1912.02781.

[36] H. Zhang, M. Cisse, Y. N. Dauphin, and D. Lopez-Paz, “Mixup: Beyond empirical risk minimization,” 2017, arXiv:1710.09412.

[37] S. S. Bamber, A. V. R. Katkuri, S. Sharma, and M. Angurala, “A hybrid CNN-LSTM approach for intelligent cyber intrusion detection system,” Comput. Secur., vol. 148, Jan. 2025, Art. no. 104146.

[38] H. I. Cos¸ar, C¸ . Arisoy, and H. Ulutas¸, “Intrusion detection on CSE-CIC-IDS2018 dataset using machine learning methods,” Artif. Intell. Theory Appl., vol. 4, no. 2, pp. 143–154, 2024.

[39] R. Rabih, H. Vahdat-Nejad, W. Mansoor, and J. H. Joloudari, “Highly accurate anomaly based intrusion detection through integration of the local outlier factor and convolutional neural network,” Sci. Rep., vol. 15, no. 1, p. 21147, Jul. 2025.

[40] K. A. E. AbdElkader, T. A. Mahmoud, T. M. Ghoniemy, and S. I. Morsy, “A multi-modal deep learning fusion approach for encrypted transport layer protocol classification,” Social Sci. Res. Netw. (SSRN), Elsevier, Tech. Rep., 2024. [Online]. Available: https:// ssrn.com/abstract=5829097

[41] J. Wu, T. Liu, and S. Zhang, “QUIC abnormal trafic detection in power grid communication system: Trafic classification based on NGO-CNN-LSTM hybrid architecture,” in Proc. 5th Int. Conf. Internet Things Mach. Learn., May 2025, pp. 216–222.

[42] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “FS-Net: A flow sequence network for encrypted trafic classification,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Apr. 2019, pp. 1171–1179.

[43] R. Jozsa, K. Hynek, and A. Pekar, “Taming volatility: Stable and private QUIC classification with federated learning,” in Proc. 21st Int. Conf. Netw. Service Manage. (CNSM), Oct. 2025, pp. 1–5.

![](images/bc66adc9fd073bb81d208aa2d83eda63d4b9a8a9b3028c26ef3312bed0da7c2e.jpg)

Anurag Dutta (Graduate Student Member, IEEE) received the bachelor’s degree in computer science and engineering from the Government College of Engineering and Textile Technology, Serampore, India. He is currently pursuing the M.S. degree with the Department of Computer Science and Engineering, IIT Kharagpur. His research interests include artificial intelligence, machine learning, computer vision, and digital forensics, with a particular focus on algorithms for multimedia security.

![](images/d4ddcc57d93fb523433bd9d1d051a7e0c3093ec616683fc13af356e74f91a991.jpg)

Pallavi Anand received the bachelor’s degree in computer science and engineering from Aryabhatta Knowledge University, Patna, India. She is currently pursuing the M.S. degree with the Department of Computer Science and Engineering, IIT Kharagpur. Her research interests include machine learning, computer network forensics, the Internet of Things (IoT) anomaly detection, and the applications of deep learning for analysis of network trafic flow.

![](images/f0bf65c85675a1b4658d6ec8c041289735cc17b12b26c8604fe7945ff2f89eaa.jpg)

Sangita Roy (Member, IEEE) received the B.Tech. degree from West Bengal University of Technology, the M.Tech. degree from Kalinga Institute of Industrial Technology, Odissa, and the Ph.D. degree from IIT Patna. She is currently an Assistant Professor with the Department of Computer Science and Engineering, Thapar Institute of Engineering and Technology, Patiala, Punjab, India. Her research interests include computer networks, networks security, image processing, and deep learning.

![](images/0b19bc3ddf76a1062bc06a9912cabae0db3615bc4718db48a0ebe10d050d7cf5.jpg)

Rajat Subhra Chakraborty (Senior Member, IEEE) is currently a Professor with the Department of Computer Science and Engineering, IIT Kharagpur. His research interests include hardware security, VLSI design and design automation, digital content protection, and digital image forensics. He is a Senior Member of ACM. He has received several awards, including the IIT Kharagpur Outstanding Faculty Award in 2018, the IEI Young Engineers Award in 2016, the IBM SUR Award in 2015, the Royal Academy of Engineering, U.K., the RECI

Fellowship in 2014, and the IBM Faculty Award in 2012. He is the Chair of the IEEE Kharagpur Section (R10). He is an Associate Editor of IEEE TRANS-ACTIONS ON COMPUTER-AIDED DESIGN OF INTEGRATED CIRCUITS AND SYSTEMS.