# HookSteg: A Truly Lossless Steganography Based on Process Hooking for Lossy Network Channels

Mingliang Zhang , Yi Zhang , Yanmei Liu , Wentong Fan , and Xiangyang Luo

Abstract—Covert communication often relies on image steganography to transmit sensitive data such as commercial secrets. Any minor bit error can lead to catastrophic consequences, which imposes extremely high demands on the zero-error transmission of secret information. However, existing robust image steganographic schemes still fail to guarantee zeroerror recovery of secret bits when resisting hybrid attacks such as compression and scaling on social platforms. To address this issue, we propose a lossless steganographic method called HookSteg, which bypasses lossy attacks on social platforms through process hooking, thereby achieving lossless steganography. This method first identifies nodes afected by lossy attacks through tracking whether image data has been compromised. Subsequently, a method for capturing lossy attack instructions is proposed based on syntax-semantic joint features and dynamic taint tracking techniques. Finally, process hooking is utilized to bypass lossy attack instructions, ensuring the lossless transmission of secret information. Experimental results on transmission scenarios with tens of millions of daily active users, such as Youku and Kutumb, demonstrate that HookSteg is general and requires no modifications to existing steganographic algorithms. It achieves, for the first time, lossless transmission of secret information in real-world scenarios, with an average improvement in extraction accuracy of 36.63%. Additionally, its eficiency in locating attack instructions is improved by 94.34% compared to traditional manual reverse engineering methods. Furthermore, this study resolves the tradeof among embedding capacity, security, and robustness, enabling steganography to focus on enhancing security and capacity, thereby providing a general and eficient solution for lossless steganography.

Index Terms—Covert communication, image steganography, lossy channel, lossless steganography, robustness.

## I. INTRODUCTION

N TODAY’s information age, the internet and social media I have deeply penetrated every aspect of social life, greatly expanding the channels for the public to access and spread information. Alongside the convenience of communication comes the persistent challenge to privacy and security. Even when encryption is employed, both communication content and metadata remain susceptible to analysis, identification, and potential leakage [1], [2]. Furthermore, the act of communication itself is visible, and its content, even if encrypted, cannot escape the possibility of surveillance and censorship. Therefore, true communication security depends not only on the confidentiality of content but also on the invisibility of the communication act itself.

Against this backdrop, image steganography [3], as a technique for hiding information within images, ofers a viable solution. This technology exploits the statistical redundancies of human vision and digital media to hide secret information into public images for transmission over open networks [4]. Specifically, the cover image [5] refers to the original image used to conceal information, while the stego image [6] denotes the image after secret data has been hidden. Steganographic techniques not only conceal the communication content but also mask the “act of secret communication” itself, serving as an efective means of transmitting private information in public environments [7].

Unfortunately, social platforms typically apply compression, scaling, or watermarking to uploaded images to optimize bandwidth and user experience [8]. These operations often damage stego images, leading to extraction failure and severely limiting the practical application of steganography [9]. This demands that steganographic algorithms possess strong robustness to resist various unintentional or malicious processing [10].

Most existing research [9], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28] focuses on identifying robust regions or features within images and uses error-correcting codes [29] to embed secret information into them to achieve robust steganography. However, when confronted with the complex and varied mixed attacks present in real-world scenarios, such methods often fail to ensure the complete extraction of the hidden information, and thus cannot be considered truly robust steganographic solutions. In sensitive data transmission scenarios with extremely high requirements for information integrity, true lossless steganography is urgently needed under lossy channels.

To address this, we propose a lossless steganographic method based on process hooking, serving as a general and eficient solution. It can provide truly lossless recovery capabilities in social platforms. The distinction between the proposed method and existing methods is illustrated in Fig. 1. By modifying the image processing logic on the client side through process hooking, our method cleverly bypasses the lossy attacks, thereby achieving lossless transmission of the secret information.

![](images/490fbc57ab62a9378a696efaca4dfb74f037d8d7306a3f88fb29544e3427279a.jpg)  
(a) Ordinary channel used by existing steganographic methods

![](images/bd43b35c483b8ea546cbc985229c6bd65eb205335a6a07773c64c6ddea0da4c5.jpg)  
(b) Proposed HookSteg channel  
Fig. 1. The diferences between the current works and HookSteg.

The main contributions of this paper are as follows:

• A steganographic method based on process hooking bypassing lossy attacks is proposed to address the issue of achieving lossless transmission of stego images under hybrid attacks in real-world scenarios. For the first time, this method realizes lossless and reliable information transmission in complex attack environments. The proposed method exhibits strong universal adaptability, improving the average extraction accuracy by 36.63% without requiring any modifications to existing steganographic algorithms, guaranteeing lossless transmission of secret information.

• An attack node identification method for stego images is designed to provide core technical support for subsequent attack instruction tracing and localization. This method innovatively integrates dynamic and static dual-analysis mechanisms to locate the critical communication nodes causing information transmission loss throughout the entire image processing workflow. Experimental validation demonstrates that this method can efectively detect and verify attack nodes in 76.66% of target platforms, filling the gap in locating the sources of attacks against stego images.

• An attack instruction localization algorithm based on syntax-semantic joint features is proposed to eficiently filter and identify attack instructions from large-scale program instruction sets. This algorithm constructs an automated filtering mechanism for decompiled statements, leveraging joint feature constraints from both syntactic and semantic dimensions, combined with dynamic taint tracking technology. It enables rapid identification of attack instructions, directly filtering out 94.34% of non-image-processing irrelevant statements, significantly enhancing the eficiency and precision of attack instruction identification.

The remainder of this paper is organized as follows. Section II presents the research background and related work. In Section III, we provide a comprehensive description of

![](images/88a8e6693929e291d4e17684ecf6be64cf9a931f94827f8031b8f59dfec2c2f9.jpg)  
Fig. 2. Market share of mobile device operating systems.

HookSteg. Section IV demonstrates the efectiveness of Hook-Steg in principle. Section V validates the efectiveness of HookSteg through experiments. Section VI concludes the paper. Finally, Section VII discusses future work.

## II. BACKGROUND AND RELATED WORK

This section reviews the research background and related work.

## A. Threat Model

Due to the convenience of mobile devices, users often rely on them to access social platforms. The mobile operating system, which includes Android, iOS, Samsung, among others, serves as the core of modern mobile devices. It not only determines the basic functionality of the device but also influ ences the user experience and application (app) ecosystem. Fig. 2 shows the market share of mobile device operating systems, with data sourced from StatCounter, an authority in trafic statistics and analysis services. It indicates that over the past three years, the Android operating system has maintained a market share of over 70.48%, demonstrating its dominant position in the market. For ease of explanation, this paper discusses and experimentally validates HookSteg on the widely used Android operating system.

This paper considers a threat model involving two parties:

• The sender possesses a mobile device with root privileges and obtains permission to execute process hooking, using this device to upload stego images to a social platform client.

• The receiver, utilizing a conventional mobile device or a web browser, completes legitimate login using the social platform account credentials provided by the sender, thereby enabling the download of stego images.

## B. Related Work

This section reviews related work in image steganography, including modification-based image steganography, mapping-based image steganography, and generation-based image steganography.

1) Modification-Based Image Steganography: Modification-based image steganography embeds secret information by modifying the pixels or coeficients of a cover image [30] and employs specific optimization strategies along with error-correction mechanisms. For instance, the robust tri-stage TLM-DNA coding scheme proposed by Alexan et al. [29] significantly enhances robustness against lossy channel attacks. These ensure that the secret information can still be extracted after being transmitted through lossy channels. Early studies [31] primarily focus on heuristically designed strategies that balance the security and robustness of steganography by selecting and modifying coeficients in transform domains such as the discrete cosine transform (DCT) and discrete wavelet transform (DWT), or pixels in the spatial domain. To address channel attacks such as JPEG recompression that may occur during actual transmission, researchers further introduce dither modulation [32], [33] and adaptive error correction coding [11], [34], aiming to ensure robustness while reducing the magnitude of modifications and enhancing security.

Additionally, some studies [12], [13] improve robustness by recompressing images. In recent years, with the development of deep learning, robust steganographic methods [9], [13] based on deep neural networks have become a research hotspot. Such methods adaptively embed secret information into cover images and introduce techniques such as noise layers and attention mechanisms. This enables the model to automatically learn to hide information in complex texture regions and enhance robustness against various types of noise, thereby improving both security and anti-interference capabilities. Modification-based embedding algorithms ofer strong robustness against specific or multiple image processing attacks. However, they inevitably introduce distortion to the cover image, which can lead to the leakage of steganographic traces and fails to ensure lossless transmission of secret information over lossy channels.

2) Mapping-Based Image Steganography: Early mappingbased image steganography draws inspiration from image retrieval [14], [15], establishing a one-to-one correspondence between specific secret information and visual features of each image, such as color histograms [35], SIFT feature points [36], or hash sequences. As the images themselves remain unmodified, these methods can resist steganalysis [37]. However, it is challenging to construct an image database that exhaustively covers all possible information fragments, and feature instability can lead to mapping mismatches. To address these issues, subsequent research [16], [17] introduces the combination of robust hashing [38] and error correction coding, designing perceptual hashing algorithms that are more robust to image processing operations to tolerate minor deviations during feature extraction.

In recent years, with the advancement of deep learning technologies, this field has further evolved into a mapping paradigm based on deep features [18], [19], [20], [21]. This approach utilizes deep neural networks to extract more discriminative and robust mid-level semantic features from images. It then constructs denser, more stable codebooks in high-dimensional feature spaces through clustering or quantization, significantly enhancing robustness against complex channel attacks. Although mapping-based image steganography exhibits strong robustness, its hiding capacity is relatively limited, which to some extent restricts the application potential of this type of method in large-scale data transmission scenarios.

3) Generation-Based Image Steganography: Generationbased image steganographic methods [22], [23], [24], [25], [26], [27], [28] have attracted increasing research attention in recent years. These methods primarily utilize generative models such as Generative Adversarial Networks (GANs) [39] and difusion models [40], [41], [42] to hide secret information directly during the image generation phase, achieving a shift from modifying the cover to generating the cover. Early research was mainly based on GANs [23], [43], which fit the real data distribution through the dynamic game between a generator and a discriminator, ofering high generation eficiency as well as good concealment and robustness. However, these methods still sufer from issues such as unrealistic synthetic images, training instability, and mode collapse [22], [44].

To overcome these limitations, recent studies have begun exploring steganographic methods based on difusion models [28], [45]. These methods generate high-quality and diverse samples through gradual denoising, avoiding mode collapse and making the secret information more concealed and natural. Nevertheless, difusion models exhibit numerical instability and sensitivity to perturbations during the generation process [25], resulting in insuficient robustness in the recovery of secret information, especially when facing unknown channel attacks.

## III. PROPOSED METHOD

To achieve lossless transmission of secret information over lossy channels, we propose an eficient and highly general lossless steganographic method that cleverly circumvents potential interference from apps with stego images by hooking the instructions used for image attacks. Without altering existing steganographic methods, HookSteg provides a genuinely lossless remedy for all schemes that break down in real-world scenarios.

## A. Overview of HookSteg

The HookSteg, illustrated in Fig. 3, consists of two main parts: the preprocessing process and the covert communication process. The preprocessing process includes three steps: identify attack nodes, extract suspicious functions, and locate lossy functions. The covert communication process comprises two steps: send secret information and extract secret information.

The core objective of the preprocessing process is to accurately locate the instructions that attack the image. It then identifies the function where these instructions reside, referred to as the lossy functions, to provide support for subsequently bypassing the lossy attacks. This process first verifies whether the stego image is only attacked on the app’s client side. If the stego image is only attacked on the client side, it utilizes syntax-semantic joint features to filter relevant image processing instructions. Subsequently, based on the obtained instructions, it extracts suspicious statements with the aid of image processing features. Then, combined with dynamic taint tracking technology, it hooks the process of the suspicious function to be verified on the client side and sends the stego image to trigger this function. Finally, an attempt is made to modify the triggered function. If the function can be successfully modified so that it no longer attacks the stego image, it is identified as the lossy functions. If the function cannot be modified, the next function from the call stack is retrieved and tested, repeating the process until the lossy functions are successfully identified.

![](images/de5842f888d5c4711c71bf0df7050320afc8cadf6d39c96d6da387881fdf4bab.jpg)  
Fig. 3. The diagram of HookSteg.

In covert communication, the core task for the sender is to ensure that the stego image retains the secret information intact even after being processed by social platforms. At this stage, the lossy functions identified during the preprocessing phase play a critical role. The sender will intercept the call to the lossy function using hooking technology and bypass this function in a zero-copy manner, thereby avoiding attacks on the image. For the receiver, the process is relatively straightforward and does not require any complex configuration. The receiver only needs to analyze the obtained image using a pre-agreed extraction algorithm, just like an ordinary user, to accurately and completely restore the information transmitted by the sender.

## B. Identify Attack Nodes

For diferent social media platforms, the nodes (serverside, client-side) and methods of image processing vary significantly. Some platforms perform processing only at the client-side node, whereas others apply it at both client and server nodes. The operations themselves also difer ranging from compression and rescaling to watermark injection.

In order to verify whether a specific app can establish a HookSteg lossless channel, we need to analyze and identify the execution nodes of lossy functions to provide support for the subsequent construction of the lossless channel. Hook-Steg employs a dual validation approach primarily based on Man-in-the-Middle (MitM) attacks, supplemented by extended Berkeley Packet Filter (eBPF) technology. The schematic diagram is shown in Fig. 4.

Let C denote the client, S the server, and M the MitM node. $\scriptstyle { \mathrm { R e q } } _ { C \to S }$ represents the connection request sent from C to S . $I _ { s }$ is the stego image generated by the sender. I<sup>0</sup> denotes the image after client-side processing, and $I _ { s } ^ { \prime \prime }$ denotes the final image downloaded from the platform.

The original communication link is:

$$
C \leftrightarrow S.\tag{1}
$$

After the MitM attacks, it becomes:

$$
C \leftrightarrow M \leftrightarrow S.\tag{2}
$$

The process for identifying the nodes of the attack image via MitM attacks consists of the following five steps:

Connection establishment request: C sends a connection request $\scriptstyle { \mathrm { R e q } } _ { C \to S }$ to S .

MitM interception: M intercepts $\scriptstyle { \mathrm { R e q } } _ { C \to S }$ , forges a response to make C believe it has connected to S , while simultaneously M initiates a connection to S , establishing the M ↔ S link.

![](images/103ab51a0ba050f0706d7f1dc8ba378dd7b935772319748a947f822b790477c0.jpg)  
Fig. 4. Schematic diagram of identifying attack nodes.

Image data upload: C processes the stego image $I _ { s }$ through operations such as compression and scaling to generate a processed image $\pmb { I } _ { s } ^ { \prime } ,$ and sends it to S .

Image interception and storage: M intercepts $I _ { s } ^ { \prime } ,$ can store it, and forwards it to S to maintain communication.

Determination of the attack nodes: Download the final image $\pmb { I } _ { s } ^ { \prime \prime }$ from the platform and compare the pixel matrices of $\pmb { I } _ { s } ^ { \prime }$ and $I _ { s } ^ { \prime \prime }$ . If $I _ { s } ^ { \prime } \equiv \bar { I } _ { s } ^ { \prime \prime }$ , it indicates client-side-only processing, enabling the establishment of a HookSteg lossless channel. If $I _ { s } ^ { \prime } \mathbf { \equiv } I _ { s } ^ { \prime \prime }$ , it signifies server-side participation in processing, preventing the establishment of a HookSteg lossless channel.

When MitM attacks are not feasible, eBPF is used to capture client-side local image data. Let the client process be $P _ { c }$ and the server process be $P _ { s }$

eBPF program loading: Write an eBPF program $E ,$ load it into the kernel, and monitor $P _ { c } { ' } s$ network communication.

Data packet filtering: E filters packets according to rules (such as destination port and protocol type) and captures only the trafic from $P _ { c }  P _ { s }$

Image data extraction: When $P _ { c }$ sends image data $I _ { s } ,$ E extracts image data blocks $B _ { 1 } , B _ { 2 } , . . . . , B _ { n }$ from the network bufer and reassembles them into the complete image ${ { I } _ { s } } ^ { \prime }$

Data storage: Write ${ { I } _ { s } } ^ { \prime }$ to storage media for subsequent comparison.

Determination of the attack nodes: Similarly, by comparing the pixel matrices of $\pmb { I } _ { s } ^ { \prime }$ and the downloaded image ${ { I } _ { s } } ^ { \prime \prime }$ , determine whether the processing mechanism involves the server side.

TABLE I  
COMMON IMAGE PROCESSING FEATURE CODES

<table><tr><td>No.</td><td>Image processing type</td><td>Operation feature code</td></tr><tr><td>1</td><td>Compression</td><td>“compress”</td></tr><tr><td>2</td><td>Rotation</td><td>“rotate”</td></tr><tr><td>3</td><td>Scaling</td><td>“resize”</td></tr><tr><td>4</td><td>Upload</td><td>“upload”</td></tr></table>

## C. Extract Suspicious Functions

Although traditional methods of locating a function through static analysis and dynamic debugging are efective, they also have some obvious drawbacks. Manual analysis of the entire codebase is required, which is particularly challenging for large, complex apps where decompiled code may be dificult to comprehend and potentially obfuscated or encrypted, significantly increasing the analysis dificulty. To rapidly locate lossy functions, we propose a localization method that leverages syntax-semantic joint features.

We define three types of statements: (i) high-level statements, which are obtained through application reverse engineering and further converted into a high-level language; (ii) feature statements, which are selected from the complete set of high-level statements based on semantic features; and (iii) suspicious statements, which are further selected from the complete set of feature statements based on syntactic features.

This stage can be divided into two sub-steps: Search for High-Level Statements (SHS) and Extract Suspicious Statements (ESS), formally represented as:

$$
\begin{array}{l} S _ {v} = \operatorname{SHS} (S _ {h}, P), \\ S _ {c} = \operatorname{ESS} (S _ {v}, R), \end{array}\tag{3}
$$

(4)

where $S _ { h } , \ S _ { \nu } ,$ , and $S _ { c }$ are the sets of high-level statements, feature statements, and suspicious statements, respectively, and the elements in these sets are denoted as $s _ { h } .$ $s _ { \nu } ,$ and $s _ { c } ,$ respectively. $S _ { \nu }$ is the set preliminarily filtered by the semantic features of image processing, and $S _ { c }$ is a set further extracted from $S _ { \nu }$ containing target statements. $P$ represents the set of semantic features for image processing, and R represents the set of syntactic features for image processing. Their elements are denoted by $p$ and r respectively. Let $\mathrm { S H S } ( S _ { h } , P )$ denote the filtering process that selects statements from $S _ { h }$ based on $P ,$ yielding $S _ { \nu } .$ Let $\mathrm { E S S } ( S _ { \nu } , R )$ denote the further filtering process that selects statements from $S _ { \nu }$ based on $R ,$ yielding $S _ { c }$

In the SHS stage, the binary app needs to be reverseengineered into assembly language and then further converted into a high-level language. Based on the semantic feature codes of image processing (as shown in Table I), the feature statement set is obtained. This process can be formally expressed as:

$$
S _ {v} = \{s _ {h} \in S _ {h} \mid \exists p \in P, p \in S _ {h} \}.\tag{5}
$$

To further narrow the filtering scope, the statements are segmented according to their syntactic features, as illustrated in Fig. 5.

The feature statement set $S _ { \nu }$ is further extracted by $R ,$ and these statements are added to the suspicious statements set $S _ { c } ,$ which can be formally expressed as:

$$
S _ {c} = \{s _ {v} \mid \exists s _ {v} \in S _ {v}, r \in R \}.\tag{6}
$$

![](images/7ef038762308e0b74b4bc7fc3fd19f6e20479d2b0c8a47df9c61c7fe7e38d78c.jpg)  
Fig. 5. Statement format.

TABLE II  
STRATEGY OF HOOKING FOR BYPASSING ATTACKS ON STEGO IMAGES

<table><tr><td>No.</td><td>Hooking strategy</td><td>Implementation method</td></tr><tr><td>1</td><td>Modify image processing logic</td><td>Replace method parameters</td></tr><tr><td>2</td><td>Modify image processing logic</td><td>Intercept method execution</td></tr><tr><td>3</td><td>Modify image processing logic</td><td>Construct return object</td></tr><tr><td>4</td><td>Modify image upload logic</td><td>Replace method parameters</td></tr></table>

We designate any function that contains suspicious statements as a suspicious functions. Extracting such functions provides crucial support for locating lossy functions.

## D. Locating Lossy Functions

To locate the lossy functions, we adopt a dynamic trigger mechanism based on hooking technology and combine it with call stack backtracking for analysis. At the same time, dynamic taint tracking technology is introduced to trace the source of suspicious functions within the API call sequence during image processing.

The interception operation implemented by the hooking technique is denoted by Hook(·). During the $\mathrm { { a p p } ^ { \prime } { s } }$ image upload operation, the function $s _ { c } ^ { i }$ corresponding to the i-th statement in ${ \cal { S } } _ { c } = \{ s _ { c } ^ { 0 } , s _ { c } ^ { 1 } , . . . , s _ { c } ^ { i } , . . . \}$ is monitored via Hook(·). When a certain function ${ s } _ { c } ^ { i }$ (referred to as the triggered function) is invoked, its input parameters, return value, and its corresponding call stack $S _ { i }$ are recorded. The call stack $S _ { i } = \{ s _ { i } ^ { 0 } , \bar { s } _ { i } ^ { 1 } , . . . , \bar { s } _ { i } ^ { n - 1 } \}$ has the function directly manipulating the image, $s _ { i } ^ { 0 }$ , at the top of the stack, while the remaining $s _ { i } ^ { 1 } , s _ { i } ^ { 2 } , \ldots$ are downstream functions within the call stack.

To bypass attacks on the stego image, we intervene in the triggered function or the functions in its call stack according to the hooking strategies L listed in Table II. Specifically, the hooking of the image processing process is achieved by modifying the image processing logic $( \mathrm { e . g . }$ , replacing method parameters, constructing return objects, intercepting method execution) and modifying the image upload logic (e.g., replacing the uploaded image path).

During the call stack backtracking phase, for the call stack corresponding to the i-th suspicious function $s _ { c } ^ { i } .$ , we start from the top function $s _ { i } ^ { 0 }$ and sequentially attempt to apply the hooking strategies, determining whether the attack can be bypassed without causing program exceptions. If $s _ { i } ^ { 0 }$ cannot be bypassed, we continue the same judgment for ${ \bf \dot { \sigma } } _ { i } ^ { 1 } , s _ { i } ^ { 2 } , \ldots$ until we find the first function $s _ { i } ^ { q }$ that can successfully bypass the image processing attack. This process can be formally represented as finding the smallest positive integer $q$ that

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Localization Algorithm of Lossy Functions
Input: Target app, $I_s$;
Output: Lossy functions $f_i$;
1: Initialize $S_v$, $S_c$, $S_i$;
2: Decomplete the app to obtain low-level language;
3: Convert the low-level language to high-level language to obtain $S_h$;
4: Filter $S_h$ using semantic features $P$ to obtain the characteristic statements set $S_v$;
5: Filter $S_v$ using syntactic features $R$ to obtain the suspicious statements set $S_c$;
6: for all $i = \{0, 1, \ldots\}$ do
7: $S_i = \text{getMethod}(S_c, i)$; // getMethod($S_c$, i) returns the function corresponding to the $i$-th suspicious statement.
8: for all $q = \{0, 1, \ldots\}$ do
9: $s_i = S_i[q]$;
10: $s_i^q = \text{getStack}(s_i, q)$; // getStack($s_i$, q) returns the call stack of the triggered function $s_t^i$.
11: $f_l = s_i^q$;
12: if Hook($f_l$, $I_s$) == $I_s$ then
13: return $f_l$;
14: end if
15: end for
16: end for
17: return None;
</div>

satisfies:

$$
\left\{ \begin{array}{l} \boldsymbol {I} _ {s} = \boldsymbol {I} _ {s} ^ {\prime}, \text {   if   } j = q \\ \boldsymbol {I} _ {s} \neq \boldsymbol {I} _ {s} ^ {\prime}, \text {   if   } j \in [ 0, q) \end{array} \right.\tag{7}
$$

where $j$ is an integer index variable. $s _ { i } ^ { q }$ is the lossy function to be localized, and for ease of representation, it will be denoted as $f _ { l }$ in the following text.

This process can also be described by Algorithm 1. The input of this algorithm is the target app and stego image, and the output is $f _ { l } .$ getMethod(·) denotes obtaining the function corresponding to the statements in the suspicious function set $\boldsymbol { S } _ { c } ,$ , and getStack(·) denotes obtaining the call stack corresponding to the triggered function. The hooking operation Hook $( f _ { l } , \pmb { I } _ { s } )$ can be defined as:

$$
\operatorname{Hook} (f _ {l}, \boldsymbol {I} _ {s}) = \boldsymbol {I} _ {s},\tag{8}
$$

where the hooking operation intercepts the call to the lossy function $f _ { l }$ and applies an appropriate strategy from the set L (see Table II) to bypass the attack, ensuring that the stego image $I _ { s }$ is transmitted without any modification.

In summary, this method systematically identifies and verifies image processing or upload functions that can efectively protect secret information through dynamic monitoring and stack structure analysis, thereby achieving accurate localization and bypassing of lossy functions.

## E. Covert Communication Process

In the covert communication phase, the sender first inputs the secret information m and the cover image $I _ { c }$ into the specified steganographic algorithm to obtain the stego image $\boldsymbol { { I } } _ { s } ,$ which can be formally represented as:

$$
\boldsymbol {I} _ {s} = \operatorname{Hide} (\boldsymbol {I} _ {c}, m),\tag{9}
$$

where Hide(· ·) is the information hiding function.

Subsequently, based on the obtained lossy function $f _ { l } ,$ we intercept it, modify the image processing pipeline, and upload the stego image $I _ { s }$ to the social-platform server, which can be formally expressed as:

$$
S \leftarrow \operatorname{Upload} (\operatorname{Hook} (f _ {l}, I _ {s})),\tag{10}
$$

where S denotes the server, and Upload(·) denotes the image upload function.

However, not all stego images have higher extraction accuracy before being attacked than after; for details, refer to Experiment V-D.2. Therefore, the following adaptive bypassing strategy can be employed to handle the stego image:

$$
S \leftarrow \left\{ \begin{array}{l l} \text {Upload(Hook(f_{l} ,I_{s}))}, & e _ {a} > e _ {u} \\ \text { Upload(I_{s})}, & e _ {a} \leq e _ {u} \end{array} \right.,\tag{11}
$$

where $e _ { a }$ represents the extraction accuracy of the stego image after being attacked, and $e _ { u }$ represents the extraction accuracy of the stego image without being attacked. Specifically, this strategy first pre-attacks the stego image and detects the extraction accuracy before and after the attack. If the extraction accuracy decreases, the bypass strategy is adopted. If the accuracy improves, the social app’s conventional image processing flow is executed when transmitting the stego image.

After the stego image is published on the social platform, the receiver can retrieve the sender’s images to obtain the stego image and use the corresponding steganographic method to completely extract the secret information sent by the sender.

$$
m ^ {\prime} = \operatorname{Ext} (I _ {s} ^ {\prime}),\tag{12}
$$

where $m ^ { \prime }$ denotes the extracted secret information, and Ext(·) is the extraction function corresponding to Hide(· ·).

It is worth noting that whether $m ^ { \prime }$ equals m depends on the specific steganographic algorithm. In the absence of attacks, if the steganographic algorithm can ensure the complete extraction of the secret information from the stego image, then $m ^ { \prime } = m ;$ otherwise, $m ^ { \prime } \ne m$ . This means that HookSteg can only guarantee the lossless transmission of secret information, provided that the secret information itself is extractable in the original channel. In other words, if the information cannot be completely extracted from the stego image even in the absence of attacks, then HookSteg likewise cannot ensure the complete extraction of the information.

## IV. PERFORMANCE ANALYSIS

This section analyzes the proposed method from three aspects: losslessness, time complexity, and memory (space) complexity, demonstrating the efectiveness of the proposed method in principle.

## A. Losslessness Analysis

Theorem 1: Lossless Channel Theorem. Under the Hook-Steg, by intercepting the lossy function $f _ { l } ,$ the sender can ensure that the secret information $m ^ { \prime }$ extracted after the stego image $I _ { s }$ is processed by the social platform is completely identical to the original information m.

Proof: Let the original image be $\textstyle I _ { c } ,$ , the secret information be m, the hiding algorithm be Hide $( I _ { c } , m ) \ \to \ I _ { s } ,$ and the extraction algorithm be $\operatorname { E x t } ( I _ { s } ^ { \prime } )  m$

(1) Sender-side Process. Define the image processing pipeline as a function composition:

$$
F = f _ {n} \circ f _ {n - 1} \circ \dots \circ f _ {0},\tag{13}
$$

where $" \mathrm { _ O } ^ { \bullet \bullet }$ denotes function composition. $f _ { 0 } , . . . , f _ { n }$ are lossless operations such as network transmission and protocol encapsulation apart from $f _ { l } .$

Then the actual processing pipeline becomes:

$$
F ^ {\prime} = f _ {n} \circ \dots \circ f _ {l + 1} \circ \operatorname{Hook} (f _ {l}, \cdot) \circ f _ {l - 1} \circ \dots \circ f _ {0}.\tag{14}
$$

Since Hook $( f _ { l } , \pmb { I } _ { s } )$ directly returns the input for the stego image, and all functions after $f _ { l }$ operate on the original stego image, therefore:

$$
\begin{array}{c} F ^ {\prime} (\boldsymbol {I} _ {s}) = f _ {n} (\boldsymbol {I} _ {s}) \circ \dots \circ f _ {l + 1} (\boldsymbol {I} _ {s}) \circ \operatorname{Hook} (f _ {l}, \boldsymbol {I} _ {s}) \\ \circ f _ {l - 1} (\boldsymbol {I} _ {s}) \circ \dots \circ f _ {0} (\boldsymbol {I} _ {s}). \end{array}\tag{15}
$$

(2) Receiver-side Process. Define the deterministic encoding function $D ( \cdot )$ (such as format encapsulation, network coding, etc.) that does not alter image content. The actual received image is:

$$
\boldsymbol {I} _ {r} = D \left(F ^ {\prime} \left(\boldsymbol {I} _ {s}\right)\right).\tag{16}
$$

The extraction algorithm Ext(·) satisfies the robustness condition:

$$
\forall \boldsymbol {I} _ {s} ^ {\prime}, \text {   if   } \operatorname{SSIM} (\boldsymbol {I} _ {s} ^ {\prime}, \boldsymbol {I} _ {s}) > \theta , \text {   then   } \operatorname{Ext} (\boldsymbol {I} _ {s} ^ {\prime}) = \operatorname{Ext} (\boldsymbol {I} _ {s}),\tag{17}
$$

where $\theta$ is the image similarity threshold, and SSIM (Structural Similarity Index Measure) is a metric for assessing the similarity between two images. When the SSIM value is 1, the two images can be considered identical.

(3) Losslessness Derivation. From Eq. 17, the attack from the lossy function $f _ { l }$ is not included, therefore:

$$
F ^ {\prime} (I _ {s}) = I _ {s}.\tag{18}
$$

For common social platforms, $D ( \cdot )$ does not alter image content, hence:

$$
\operatorname{SSIM} \left(\boldsymbol {I} _ {r}, \boldsymbol {I} _ {s}\right) = 1 > \theta .\tag{19}
$$

Therefore:

$$
m ^ {\prime} = \operatorname{Ext} (\boldsymbol {I} _ {r}) = \operatorname{Ext} (\boldsymbol {I} _ {s}) = m.\tag{20}
$$

HookSteg does not modify any pixel values or image metadata. It only redirects the control flow of the application. Consequently, it introduces no additional artifacts to the stego image. The transmitted image is bitwise identical to the original stego image generated by the steganographic algorithm.

## B. Time Complexity Analysis

Theorem 2: Processing Time Complexity Theorem. For any stego image $I _ { s } ,$ the processing time $T _ { \mathrm { h o o k } }$ of the HookSteg channel is constant. In contrast, the processing time T<sub>conventional</sub> of the conventional channel is linearly related to the total number of image pixels n, namely:

$$
T _ {\text { hook }} = O (1) <   T _ {\text { conventional }} = O (n).\tag{21}
$$

Proof: (1) Time Complexity of Conventional Channel. A conventional image processing pipeline includes operations such as scaling and compression, and its time complexity is:

$$
T _ {\text { conventional }} = \sum_ {i = 0} ^ {k} T _ {f _ {i}} (\boldsymbol {I} _ {s}) = O (n),\tag{22}
$$

where n is the total number of pixels. Scaling and compression algorithms need to traverse all pixels, hence $T _ { f _ { i } } = O ( n )$

(2)Time Complexity of HookSteg Channel. HookSteg bypasses the lossy function $f _ { l }$ through kernel-level hooking, and the actual execution sequence is:

$$
\begin{array}{c} P _ {\text {hook}} (\boldsymbol {I} _ {s}) = f _ {k} (\boldsymbol {I} _ {s}) \circ \dots \circ f _ {l + 1} (\boldsymbol {I} _ {s}) \circ \text {Hook} (f _ {l}, \boldsymbol {I} _ {s}) \\ \circ f _ {l - 1} (\boldsymbol {I} _ {s}) \circ \dots \circ f _ {0} (\boldsymbol {I} _ {s}), \end{array}\tag{23}
$$

where $f _ { 0 } , \ldots , f _ { k }$ are lossless operations such as network transmission and protocol encapsulation, with a time complexity of O(1).

The hooking framework’s own overhead $T _ { \mathrm { o v e r h e a d } }$ includes conditional checking, control flow transfer, and context restoration, all of which are constant-time operations.

Therefore:

$$
\begin{array}{r l} T _ {\text { hook }} & = T _ {\text { overhead }} + \sum_ {j = 0} ^ {k} T _ {f _ {j}} (\boldsymbol {I} _ {s}) \\ & = O (1) + O (1) = O (1). \end{array}\tag{24}
$$

(3) Quantification of Time Advantage. The ratio of pro cessing time between the two channels is:

$$
\eta = \frac {T _ {\mathrm{conventional}}}{T _ {\mathrm{hook}}} = \frac {O (n)}{O (1)} = \Omega (n),\tag{25}
$$

where $\Omega ( n )$ denotes the asymptotic lower bound, indicating that the time advantage over conventional methods grows at least linearly with the image size, highlighting its significant superiority in large-scale image processing.

By circumventing pixel-level processing with O(n) complexity, HookSteg reduces the processing time of stego images to a constant level, achieving theoretically optimal eficiency.

## C. Memory Complexity Analysis

To evaluate the practical feasibility of HookSteg, we analyze its memory complexity in this subsection. The memory overhead of HookSteg primarily originates from three sources: (i) the hooking framework itself, (ii) the dynamically generated hook stubs and trampolines, and (iii) the temporary storage of call stack information during the preprocessing phase.

Theorem 3: Memory Complexity Theorem. For any stego image $I _ { s } ,$ , the memory consumption $M _ { \mathrm { h o o k } }$ of the HookSteg channel is constant and independent of the image size n (where n) is the total number of pixels). In contrast, a conventional image processing channel has a memory complexity of O(n).

Proof: (1) Memory Complexity of Conventional Channel. A conventional image processing pipeline involves operations such as decompression, scaling, and recompression. These operations typically require the image to be fully or partially loaded into memory. For an image with n pixels, the memory footprint is at least proportional to n. Formally,

$$
M _ {\text { conventional }} = O (n).\tag{26}
$$

(2) Memory Complexity of HookSteg Channel. HookSteg bypasses the lossy function f<sub>l</sub> by intercepting its call at the kernel or user-space level. The hooking mechanism (e.g., inline hooking or function detouring) introduces:

• A fixed-size jump instruction (typically 5–14 bytes on ARM/ARM64).

• A trampoline function that restores the original control flow (constant size).

• A small hook context structure, also constant.

All of these overheads are independent of the image pixel count n. Additionally, the temporary call stack captured during the preprocessing phase (Algorithm 1) stores only function addresses and return addresses, whose number is bounded by the maximum call stack depth (a constant). Therefore,

$$
M _ {\mathrm{hook}} = O (1).\tag{27}
$$

(3) Quantification of Memory Advantage. The memory ratio between the conventional channel and the HookSteg channel is

$$
\mu = \frac {M _ {\text { conventional }}}{M _ {\text { hook }}} = \frac {O (n)}{O (1)} = \Omega (n),\tag{28}
$$

which grows at least linearly with the image size. For highresolution images, the memory saving is several orders of magnitude.

This analysis demonstrates that HookSteg not only reduces processing time to constant but also eliminates the memory footprint required for pixel-level transformations, making it highly practical for resource-constrained mobile devices.

## V. EXPERIMENTS

In this section, we conduct experiments to evaluate the performance of HookSteg. The experiments primarily include the experimental setup, identification of attack nodes, localization eficiency of lossy functions, robustness, and transmission eficiency.

## A. Experimental Setup

During the experiment, we use a One Plus Ace2 as the real device and validate HookSteg in an actual network environment. The device runs the Android 13 operating system. To enable in-depth testing and analysis of the proposed method, we employ the hooking tool Frida within a Python environment, utilize the Objection tool for real-time monitoring of function execution, and adopt Reqable as the network data analysis tool. Detailed experimental environment information is provided in Table IV.

For modification-based steganographic methods, the Boss-Base v1.01 [46] dataset is adopted, with 1,000 images used for each method. Their resolutions are uniformly adjusted to $5 , 0 0 0 \times 5 , 0 0 0$ pixels to test large-capacity scenarios, and they are saved as JPEG images with quality factors $( Q _ { f } )$ of 75 and 85, respectively. For generation-based steganographic methods, 1,000 images are also used, following the original experimental settings of each method and adopting their corresponding publicly available pre-trained models. The specific parameter configurations are shown in Table V.

## B. Identification of Attack Nodes

To evaluate the performance of HookSteg in identifying attack nodes, we select the top 50 apps from China’s largest third-party mobile app store, “Yingyongbao”, and filter out 21 apps that can interact through images as experimental subjects. In addition, we select 7 international mobile apps accessible in China from the Google Play Store. The apps’s information and experimental results are shown in Table III. In the experiment, we use MitM attacks (denoted $\boldsymbol { \mathrm { b y } } ^ { \bullet } ( \bullet \cdot \boldsymbol { \sigma } ^ { \bullet } )$ and eBPF (denoted by “ ”) to identify nodes where images are attacked. When the former is unavailable, the latter is used as a supplementary means. When the nodes where images are attacked cannot be identified, it is denoted by “ ”. The experimental results also classify the attack nodes of the images, including client-only attacks, server-involved attacks, and neither client nor server attacks.

TABLE III  
IDENTIFICATION OF ATTACK NODES. (THE TABLE DATA IS AS OF JANUARY 1, 2026. THE SAME APPLIES TO THE FOLLOWING)

<table><tr><td>App name</td><td>Download count</td><td>Package name</td><td>Version</td><td>Type</td><td>Validation method</td><td>Client-side only</td><td>Server-side involved</td><td>No processing</td></tr><tr><td>Facebook</td><td>10B+</td><td>com.facebook.katana</td><td>501.0.0.61.70</td><td>Social</td><td>○</td><td>-</td><td>-</td><td>-</td></tr><tr><td>X</td><td>1B+</td><td>com.twitter.android</td><td>10.81.0-release.0</td><td>Social</td><td>○</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Pinterest</td><td>1B+</td><td>com.pinterest</td><td>13.6.0</td><td>Social</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Reddit</td><td>100M+</td><td>com.reddit.frontpage</td><td>2025.07.1</td><td>Social</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Tumblr</td><td>100M+</td><td>com.tumblr</td><td>38.3.0.110</td><td>Image</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Quora</td><td>50M+</td><td>com.quora.android</td><td>3.2.30</td><td>Q&amp;A</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Kutumb</td><td>50M+</td><td>com.kutumb.android</td><td>7.1.7</td><td>Social</td><td>●</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Medium</td><td>10M+</td><td>com.medium.reader</td><td>4.5.1253348</td><td>Social</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Hiferr</td><td>1M+</td><td>com.hiferr</td><td>1.0.37</td><td>Social</td><td>●</td><td>√</td><td>×</td><td>×</td></tr><tr><td>QQ</td><td>9B+</td><td>com.tencent.mobileqq</td><td>9.1.50</td><td>Social</td><td>○</td><td>-</td><td>-</td><td>-</td></tr><tr><td>WeChat</td><td>8B+</td><td>com.tencent.mm</td><td>8.0.56</td><td>Social</td><td>○</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Tencent Video</td><td>5B+</td><td>com.tencent.qqlive</td><td>9.01.25.30019</td><td>Video</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Taobao</td><td>4B+</td><td>com.taobao.taobao</td><td>10.49.10</td><td>Shopping</td><td>○</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Baidu</td><td>3B+</td><td>com.baidu.searchbox</td><td>15.0.0.10</td><td>Search</td><td>●</td><td>×</td><td>×</td><td>√</td></tr><tr><td>KuGou Music</td><td>2B+</td><td>com.kugou.android</td><td>20.1.5</td><td>Music</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Pinduoduo</td><td>2B+</td><td>com.xunmeng.pinduoduo</td><td>7.48.0</td><td>Shopping</td><td>○</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Gaode Map</td><td>2B+</td><td>com.autonavi.minimap</td><td>15.16.0.2075</td><td>Navigation</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Weibo</td><td>2B+</td><td>com.sina.weibo</td><td>15.2.2</td><td>Social</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>QQ Music</td><td>2B+</td><td>com.tencent.qqmusic</td><td>14.1.1.8</td><td>Music</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>iQiyi</td><td>2B+</td><td>com.qiyi.video</td><td>16.5.2</td><td>Video</td><td>●</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Toutiao</td><td>2B+</td><td>com.ss.android.article.news</td><td>12.3.0</td><td>News</td><td>●</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Youku</td><td>2B+</td><td>com.youku.phone</td><td>11.1.24</td><td>Video</td><td>●</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Baidu Map</td><td>2B+</td><td>com.baidu.BaiduMap</td><td>20.14.30</td><td>Navigation</td><td>●</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Meituan</td><td>1B+</td><td>com.sankuai.meituan</td><td>12.35.203</td><td>Food Delivery</td><td>○</td><td>-</td><td>-</td><td>-</td></tr><tr><td>58 Tongcheng</td><td>540M+</td><td>com.wuba</td><td>13.28.3</td><td>Trading</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Ximalaya</td><td>430M+</td><td>com.ximalaya.ting.android</td><td>9.3.40.3</td><td>Audiobook</td><td>●</td><td>×</td><td>×</td><td>√</td></tr><tr><td>QQ Reader</td><td>420M+</td><td>com.qq.reader</td><td>8.27.7.888</td><td>Reading</td><td>➊</td><td>√</td><td>×</td><td>×</td></tr><tr><td>NetEase News</td><td>410M+</td><td>com.netease.newsreader.activity</td><td>113.9</td><td>News</td><td>●</td><td>×</td><td>×</td><td>√</td></tr><tr><td>Dianping</td><td>390M+</td><td>com.dianping.v1</td><td>11.40.13</td><td>Reviews</td><td>●</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Ctrip</td><td>380M+</td><td>ctrip.android.view</td><td>8.78.6</td><td>Travel</td><td>➊</td><td>×</td><td>√</td><td>×</td></tr></table>

TABLE IV  
EXPERIMENTAL SETUP

<table><tr><td>No.</td><td>Software Name</td><td>Version</td><td>Remarks</td></tr><tr><td>1</td><td>Python</td><td>3.8.0</td><td>Base environment</td></tr><tr><td>2</td><td>Frida</td><td>16.5.9</td><td>Hooking tool</td></tr><tr><td>3</td><td>Reqable</td><td>2.30.3</td><td>Network traffic analysis tool</td></tr><tr><td>4</td><td>Objection</td><td>1.11.0</td><td>Memory exploration</td></tr></table>

TABLE V  
METHODS COMPARED AND THEIR TYPES

<table><tr><td>Method Name</td><td>Year</td><td>Format</td><td>Type</td><td>Principle Type</td><td>Resolution</td></tr><tr><td>J-UNIWARD [47]</td><td>2014</td><td>JPEG</td><td>Classical</td><td>Modification-based</td><td>5,000×5,000</td></tr><tr><td>DMAS [32]</td><td>2018</td><td>JPEG</td><td>Robust</td><td>Modification-based</td><td>5,000×5,000</td></tr><tr><td>JCRISBE [13]</td><td>2021</td><td>JPEG</td><td>Robust</td><td>Modification-based</td><td>5,000×5,000</td></tr><tr><td>SCRIPT [30]</td><td>2024</td><td>JPEG</td><td>Robust</td><td>Modification-based</td><td>5,000×5,000</td></tr><tr><td>ROAST [12]</td><td>2024</td><td>JPEG</td><td>Robust</td><td>Modification-based</td><td>5,000×5,000</td></tr><tr><td>StegaDDPM [45]</td><td>2023</td><td>TIFF</td><td>Classical</td><td>Generation-based</td><td>256×256</td></tr><tr><td>ERGI [25]</td><td>2024</td><td>PNG</td><td>Robust</td><td>Generation-based</td><td>512×512</td></tr><tr><td>PARIS [23]</td><td>2024</td><td>JPEG</td><td>Robust</td><td>Generation-based</td><td>64×64</td></tr><tr><td>GSD [28]</td><td>2025</td><td>PNG</td><td>Classical</td><td>Generation-based</td><td>64×64</td></tr><tr><td>TransStego [43]</td><td>2025</td><td>JPEG</td><td>Robust</td><td>Generation-based</td><td>400×400</td></tr></table>

The experimental results show that diferent apps have diferent approaches regarding the nodes where images are attacked. From a statistical perspective, the MitM attack method is widely used in 70.00% of social apps, indicating that this method has high applicability and efectiveness. As a supplement, the eBPF method, together with the MitM attack method, jointly verifies 76.66% of the apps. Therefore, through these two methods, we can accurately identify the attack nodes of most apps.

From the perspective of the nodes where images are attacked, we observe significant diferences in image processing strategies across diferent types of apps. For instance, apps like iQiyi and QQ Reader tend to preserve high-quality original images with superior visual efects, providing greater operational space for implementing lossless steganography. In contrast, apps such as NetEase News and Dianping prioritize storage costs and user experience, often processing images before storing them on servers. Meanwhile, apps like Kutumb and Youku handle image processing exclusively on the client side. In the following experiments, we validate HookSteg’s performance using Kutumb, Hiferr, Youku, and Kehua as test cases.

This experiment validates the applicability of HookSteg for establishing lossless channels and reveals the diferences in image processing strategies among diferent types of apps. These findings provide References for future research on image processing technologies and data protection.

## C. Localization Eficiency of Lossy Functions

To verify the efectiveness of HookSteg in locating lossy functions, we conduct experiments on the apps listed in Table III that allow attack bypass via HookSteg, including iQiyi, Toutiao, Youku, Baidu Map, QQ Reader, Kutumb, and Hiferr. The experiment precisely locates the lossy functions, and the total number of retrieved, filtered, and extracted suspicious functions for each app, along with the eficiency improvement compared to manual analysis, are sequentially presented in Figs. 6 (a), (b), (c) and (d).

![](images/c53e3cc70f379fd8f249397a2521f64855b83831f882793c36f3bcb45c70ddad.jpg)  
Fig. 6. Experiment on extraction eficiency of lossy functions.

It can be seen from the experimental results that HookSteg performs excellently in locating the lossy functions, with an average eficiency improvement of 94.34%. This indicates that the method has a significant efect in reducing unnecessary retrieval volume, thereby improving overall retrieval eficiency. Furthermore, the lossy functions for all apps are found within the extracted suspicious statements, indicating that the method can efectively identify lossy functions, ensuring the accuracy and reliability of the extracting results. The application of this method is expected to play an important role in practical retrieval tasks, greatly enhancing the eficiency of constructing lossless channels.

## D. Robustness Experiment

Regarding the selection of comparison methods, this paper focuses on two categories: modification-based steganography and generation-based steganography. Although these two types of methods ofer higher embedding capacity, they struggle to achieve lossless recovery under hybrid attacks. To validate the robustness of the proposed method under high-capacity transmission, the aforementioned methods are selected for experimentation. Mapping-based steganography, while exhibiting strong robustness, sufers from excessively low embedding capacity and fails to meet the high-capacity transmission requirements of social platforms. Therefore, it is not included in the comparison.

The real-world experimental scenarios are: Youku, Kehua, Hiferr, and Kutumb. Their respective quality factors for image processing are 80, 60, 100, and 80. The experiments are conducted on conventional channels and the HookSteg channel constructed based on our proposed method.

1) Robustness Experiment for Modification-Based Steganography: To verify the robustness of modificationbased steganographic methods in real-world scenarios, we conduct experiments under two scenarios. The first condition uses images whose compression quality factors match those observed from the actual platforms. The second condition uses images whose quality factors do not match those of the platforms. The experimental results are shown in Table VI and Table VII, where the data in the last three columns represent the extraction accuracy of stego image under no attack, under attack, and the change after attack, respectively. When the change in extraction accuracy is non-negative, it indicates that the method efectively resists the attack without decreasing extraction accuracy. Such values are highlighted in bold. It is worth noting that the Hiferr scenario uses a quality factor of 100 when compressing images. Under this condition, SCRIPT fails to generate stego images, making it impossible to calculate its extraction accuracy. The corresponding result is denoted by “-”.

TABLE VI  
ROBUSTNESS EXPERIMENT OF MODIFICATION-BASED STEGANOGRAPHY UNDER QUALITY FACTORS MATCHED TO REAL-WORLD SCENARIOS

<table><tr><td rowspan="2">App</td><td rowspan="2">Method</td><td rowspan="2">Stego↑(No attack)</td><td colspan="2">Conventional channel</td><td colspan="2">HookSteg channel</td></tr><tr><td>Attacked↑</td><td>Change↑</td><td>Attacked↑</td><td>Change↑</td></tr><tr><td rowspan="5">Youku</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.01%</td><td>-49.99%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.31%</td><td>-49.68%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>50.00%</td><td>-50.00%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>99.11%</td><td>49.92%</td><td>-49.19%</td><td>99.11%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.02%</td><td>-49.98%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Kehua</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.00%</td><td>-50.00%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.19%</td><td>-49.80%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>50.01%</td><td>-49.99%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>99.99%</td><td>50.17%</td><td>-49.82%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.00%</td><td>-50.00%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Hiferr</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.01%</td><td>-49.99%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>50.26%</td><td>49.96%</td><td>-0.30%</td><td>50.26%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>ROAST [12]</td><td>50.10%</td><td>49.93%</td><td>-0.17%</td><td>50.10%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.01%</td><td>-49.99%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Kutumb</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.02%</td><td>-49.98%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.04%</td><td>-49.95%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>50.01%</td><td>-49.99%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>98.68%</td><td>49.99%</td><td>-48.69%</td><td>98.68%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.01%</td><td>-49.99%</td><td>100.00%</td><td>0.00%</td></tr><tr><td colspan="2">Mean (All Apps)</td><td>94.64%</td><td>50.03%</td><td>-44.61%</td><td>94.64%</td><td>0.00%</td></tr></table>

When using images whose compression quality factors match those observed from the actual platforms, Table VI shows that after being transmitted through conventional channels, the extraction accuracy of stego images generated by J-UNIWARD [47], DMAS [32], SCRIPT [30], ROAST [12], and JCRISBE [13] is around 50%. This result is comparable to random guessing, making it impossible to extract efective secret information. However, after the stego images of J-UNIWARD [47], DMAS [32], SCRIPT [30], ROAST [12], and JCRISBE [13] are transmitted via HookSteg, their extraction accuracy remains consistent with that under no attack. Compared to transmission over conventional channels, the extraction accuracy improves by an average of 44.61%.

When using images whose compression quality factors do not match those observed from the actual platforms, stego images with quality factors of 75 and 85 are selected for the experiment. The experimental results are similar to those obtained when the attack parameters are known. Table VI shows that after transmission over conventional channels, the extraction accuracy of J-UNIWARD [47], DMAS [32], SCRIPT [30], ROAST [12], and JCRISBE [13] is also around 50%. After using HookSteg, the extraction accuracy of these methods is significantly improved, with an average increase of 49.72%.

By conducting experiments on J-UNIWARD [47], DMAS [32], SCRIPT [30], ROAST [12], and JCRISBE [13], this subsection verifies the robustness of modification-based steganographic methods in two scenarios. The experimental results show that, under the hybrid attacks of social platforms, the extraction accuracy of both non-robust and robust modification-based steganographic methods significantly decreases. However, when the proposed HookSteg is used, the extraction accuracy is significantly improved, with an average increase of 48.06%.

TABLE VII  
ROBUSTNESS EXPERIMENT OF MODIFICATION-BASED STEGANOGRAPHY UNDER QUALITY FACTORS MISMATCHED TO REAL-WORLD SCENARIOS

<table><tr><td rowspan="2"> $Q_f$ </td><td rowspan="2">App</td><td rowspan="2">Method</td><td rowspan="2">Stego (No attack) ↑</td><td colspan="2">Conventional channel</td><td colspan="2">HookSteg channel</td></tr><tr><td>Attacked ↑</td><td>Change ↑</td><td>Attacked ↑</td><td>Change ↑</td></tr><tr><td rowspan="20">75</td><td rowspan="5">Youku</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.71%</td><td>-49.29%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.28%</td><td>-49.71%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>50.29%</td><td>-49.71%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>99.82%</td><td>50.75%</td><td>-49.07%</td><td>99.82%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>49.97%</td><td>-50.03%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Kehua</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>49.95%</td><td>-50.05%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>49.99%</td><td>-50.00%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>50.67%</td><td>-49.33%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>99.91%</td><td>49.43%</td><td>-50.48%</td><td>99.91%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.00%</td><td>-50.00%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Hiferr</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.01%</td><td>-49.99%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.06%</td><td>-49.93%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>49.96%</td><td>-50.04%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>99.84%</td><td>49.92%</td><td>-49.92%</td><td>99.84%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.00%</td><td>-50.00%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Kutumb</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.01%</td><td>-49.99%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.22%</td><td>-49.77%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>49.97%</td><td>-50.03%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>99.89%</td><td>50.40%</td><td>-49.49%</td><td>99.89%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>49.99%</td><td>-50.01%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="20">85</td><td rowspan="5">Youku</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>49.97%</td><td>-50.03%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>49.98%</td><td>-50.01%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>50.35%</td><td>-49.65%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>98.22%</td><td>50.13%</td><td>-48.09%</td><td>98.22%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.03%</td><td>-49.97%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Kehua</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.00%</td><td>-50.00%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.12%</td><td>-49.87%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>49.31%</td><td>-50.69%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>98.30%</td><td>49.65%</td><td>-48.65%</td><td>98.30%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.00%</td><td>-50.00%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Hiferr</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>49.98%</td><td>-50.02%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.01%</td><td>-49.98%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>49.91%</td><td>-50.09%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>98.28%</td><td>49.87%</td><td>-48.41%</td><td>98.28%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.00%</td><td>-50.00%</td><td>100.00%</td><td>0.00%</td></tr><tr><td rowspan="5">Kutumb</td><td>J-UNIWARD [47]</td><td>100.00%</td><td>50.02%</td><td>-49.98%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>DMAS [32]</td><td>99.99%</td><td>50.04%</td><td>-49.95%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>SCRIPT [30]</td><td>100.00%</td><td>49.72%</td><td>-50.28%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ROAST [12]</td><td>98.97%</td><td>50.24%</td><td>-48.73%</td><td>98.97%</td><td>0.00%</td></tr><tr><td>JCRISBE [13]</td><td>100.00%</td><td>50.02%</td><td>-49.98%</td><td>100.00%</td><td>0.00%</td></tr><tr><td colspan="3">Mean ( $Q_f$ =75)</td><td>99.97%</td><td>50.13%</td><td>-49.84%</td><td>99.97%</td><td>0.00%</td></tr><tr><td colspan="3">Mean ( $Q_f$ =85)</td><td>99.69%</td><td>49.97%</td><td>-49.72%</td><td>99.69%</td><td>0.00%</td></tr></table>

2) Robustness Experiment for Generation-Based Steganography: To verify the efectiveness of HookSteg for generationbased steganographic methods, this subsection selects five representative schemes [23], [25], [28], [43], [45] for experimental evaluation. Relevant results are shown in Table VIII.

Experimental data show that the extraction accuracy of StegaDDPM [45] and GSD [28] after being attacked is around 50%. The extraction accuracy of TransStego [43], ERGI [25], and PARIS [23] is above 80%. The experimental results indicate that the non-robust generation-based steganographic methods StegaDDPM [45] and GSD [28], similar to modification-based steganographic methods, are also unable to resist attacks in real lossy environments. In contrast, the robust generation-based steganographic methods TransStego [43], ERGI [25], and PARIS [23] can resist attacks over lossy channels to varying degrees.

Furthermore, for TransStego [43] transmitted via the Hiferr scenario, the extraction accuracy after being attacked is actually higher than that of the original stego image. This is because JPEG compression, even at quality factor 100, introduces slight quantization errors. This “mild perturbation” might correct certain distribution biases or minor errors introduced during the training or generation of the generation-based steganography model. This allows the extractor to work on data closer to the training conditions, thereby increasing the accuracy. According to HookSteg’s autonomous selection strategy in the image processing flow, higher extraction accuracy is ensured. When TransStego’s stego images are transmitted via the Hiferr scenario, they still follow the conventional processing flow. This experiment demonstrates that HookSteg significantly enhances the robustness of generationbased steganographic methods, with an average improvement of 25.19%, which also verifies the efectiveness of HookSteg for these methods.

TABLE VIII  
ROBUSTNESS EXPERIMENT OF GENERATION-BASED STEGANOGRAPHIC METHODS

<table><tr><td rowspan="2">App</td><td rowspan="2">Method</td><td rowspan="2">Stego↑(No attack)</td><td colspan="2">Conventional channel</td><td colspan="2">HookSteg channel</td></tr><tr><td>Attacked↑</td><td>Change↑</td><td>Attacked↑</td><td>Change↑</td></tr><tr><td rowspan="5">Youku</td><td>StegaDDPM [45]</td><td>100.00%</td><td>50.53%</td><td>-49.47%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ERGI [25]</td><td>99.03%</td><td>91.66%</td><td>-7.37%</td><td>99.03%</td><td>0.00%</td></tr><tr><td>PARIS [23]</td><td>98.44%</td><td>90.10%</td><td>-8.34%</td><td>98.44%</td><td>0.00%</td></tr><tr><td>GSD [28]</td><td>99.99%</td><td>50.03%</td><td>-49.96%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>TransStego [43]</td><td>98.80%</td><td>98.30%</td><td>-0.50%</td><td>98.80%</td><td>0.00%</td></tr><tr><td rowspan="5">Kehua</td><td>StegaDDPM [45]</td><td>100.00%</td><td>50.42%</td><td>-49.58%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ERGI [25]</td><td>99.03%</td><td>88.06%</td><td>-10.97%</td><td>99.03%</td><td>0.00%</td></tr><tr><td>PARIS [23]</td><td>98.44%</td><td>87.50%</td><td>-10.94%</td><td>98.44%</td><td>0.00%</td></tr><tr><td>GSD [28]</td><td>99.99%</td><td>50.07%</td><td>-49.92%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>TransStego [43]</td><td>98.80%</td><td>97.60%</td><td>-1.20%</td><td>98.80%</td><td>0.00%</td></tr><tr><td rowspan="5">Hiferr</td><td>StegaDDPM [45]</td><td>100.00%</td><td>50.75%</td><td>-49.25%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ERGI [25]</td><td>99.03%</td><td>85.31%</td><td>-13.72%</td><td>99.03%</td><td>0.00%</td></tr><tr><td>PARIS [23]</td><td>98.44%</td><td>83.85%</td><td>-14.59%</td><td>98.44%</td><td>0.00%</td></tr><tr><td>GSD [28]</td><td>99.99%</td><td>49.95%</td><td>-50.04%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>TransStego [43]</td><td>98.80%</td><td>99.20%</td><td>+0.40%</td><td>99.20%</td><td>+0.40%</td></tr><tr><td rowspan="5">Kutumb</td><td>StegaDDPM [45]</td><td>100.00%</td><td>50.28%</td><td>-49.72%</td><td>100.00%</td><td>0.00%</td></tr><tr><td>ERGI [25]</td><td>99.03%</td><td>80.92%</td><td>-18.11%</td><td>99.03%</td><td>0.00%</td></tr><tr><td>PARIS [23]</td><td>98.44%</td><td>84.11%</td><td>-14.33%</td><td>98.44%</td><td>0.00%</td></tr><tr><td>GSD [28]</td><td>99.99%</td><td>50.11%</td><td>-49.88%</td><td>99.99%</td><td>0.00%</td></tr><tr><td>TransStego [43]</td><td>98.80%</td><td>92.90%</td><td>-5.90%</td><td>98.80%</td><td>0.00%</td></tr><tr><td colspan="2">Mean (All Apps)</td><td>99.25%</td><td>74.08%</td><td>-25.17%</td><td>99.27%</td><td>+0.02%</td></tr></table>

![](images/a68dbd39d140674bc319bdd2cf73ab177ce476d8202890bec2d7f64d1d3c231b.jpg)  
Fig. 7. Extraction accuracy of generation-based steganographic methods.

Fig. 7 further visualizes the above results in the form of a line chart. The horizontal axis represents four realworld scenarios, and the vertical axis represents the extraction accuracy. The red dashed line denotes the HookSteg channel, and the blue dashed line denotes the conventional channel. For modification-based steganographic methods, we show the performance of the HookSteg channel under two mismatched quality factor scenarios $( Q _ { f } = 8 5 $ and $Q _ { f } = 7 5 )$ , as well as the robustness performance under the conventional channel. For generation-based steganographic methods, we similarly present a comparison between the HookSteg channel and the conventional channel. It can be observed that the extraction accuracy of all methods under HookSteg is significantly higher than that under the conventional channel. This figure further demonstrates the robustness of HookSteg against real, unknown, and automated channel attacks.

In this subsection, experimental validation is conducted separately for modification-based steganographic methods and generation-based steganographic methods. The experimental results show that after using HookSteg, the extraction accuracy of the two types of methods achieves an average improvement of 48.06% and 25.19%, respectively, with a comprehensive average improvement of 36.63%. These results indicate that when stego images are transmitted via real-world scenarios, the proposed method enables lossless transmission of secret information and efectively enhances the robustness of steganographic methods, thereby verifying the excellent robustness performance of HookSteg.

![](images/5b64dfd5b25fd4e326aa7e1ebec4d8fd7195cbc83ae4b823650f9938f90a4d0f.jpg)

Fig. 8. Comparison experiment of transmission eficiency.  
![](images/606cbc296ec849f2fc059bebd440257ed1e2e9021016234eb4cf1ff81107cb91.jpg)  
Fig. 9. Representative images used in the experiments.

## E. Transmission Eficiency

To investigate the impact of HookSteg on the transmission eficiency of stego images, this experiment is conducted with the scaling factor fixed at 0.8 and the compression factor set to 100, 80, and 60, respectively. Four types of images with diferent resolutions are selected for the experiment: 512×512, $1 , 0 2 4 \times 1 , 0 2 4 ,$ 2 048 × 2 048, and 4 096 × 4 096 pixels. The experimental results are shown in Fig. 8.

Fig. 8 illustrates the time consumed for processing images across four groups of experiments. Among them, the first three groups of experiments are conducted in a conventional channel environment, with their attack parameters represented in the form of a tuple (quality factor, scaling factor). The fourth group shows the time required for HookSteg to process stego images.

Experimental data show that under the same attack parameters, the processing time for stego images in the conventional channel increases with image size. When the scaling factor and image size are fixed, the processing time is significantly longer for a quality factor of 100, while the times for quality factors 60 and 80 are relatively similar. In the channel established by HookSteg, the time required to process stego images is 1 millisecond, which is unafected by image size or quality factor. This is because HookSteg bypasses the conventional image processing pipeline, and its processing time is entirely determined by the overhead of the hooking framework itself.

The experimental results indicate that compared to the conventional channel, the channel established by HookSteg introduces no additional transmission burden. Moreover, by avoiding image encoding and decoding processes, it significantly improves image transmission eficiency.

## VI. CONCLUSION

This paper proposes for the first time a lossless steganographic method suitable for lossy channels, aiming to meet the high requirements for information integrity in sensitive data transmission scenarios. The method leverages process hooking to efectively circumvent lossy channel attacks, ensuring that no bit errors occur during the transmission of secret information. Experimental results show that the method enables eficient and lossless covert communication in real-world scenarios, providing strong support for the accurate transmission of high-value sensitive data. Compared with existing steganographic methods, our method efectively breaks the mutual constraints among embedding capacity, security, and robustness, allowing steganography research to focus on the enhancement of security and capacity. This method opens up a new path for the field of digital privacy protection, particularly ofering a reliable data security solution for application scenarios with extremely high requirements for information integrity.

## VII. FUTURE WORK

Although HookSteg can achieve lossless robust steganography under lossy channels, it still has two main limitations. First, HookSteg requires the sender’s device to have root privileges to perform process hooking operations, which is dificult to popularize on ordinary user devices. Future work will explore lightweight bypass solutions based on virtualization or sandboxing technologies to serve a broader range of users. Second, HookSteg is applicable only to scenarios where the image is attacked solely on the client side. For applications where lossy processing also exists on the server side, HookSteg cannot guarantee lossless transmission. Future research may incorporate prior knowledge of server-side processing to design targeted robust steganographic coding or error correction mechanisms, enabling partial tolerance of lossy operations on the server side.

## APPENDIX

## REPRESENTATIVE IMAGE SAMPLES

To provide a clear illustration of the image data used in our experiments, we present representative image samples in Fig. 9. The first image is taken from the BossBase v1.01 dataset [46], which serves as the cover images for modification-based steganographic methods. The subsequent five images are generated by the five generation-based steganographic methods (StegaDDPM [45], ERGI [25], PARIS [23], GSD [28], and TransStego [43]) using their respective publicly available pre-trained models. All images are displayed with their corresponding resolutions explicitly labeled.

## REFERENCES

[1] P. Jiang et al., “Boomerang: Metadata-private messaging under hardware trust,” in Proc. 20th USENIX Symp. Networked Syst. Design Implement. (NSDI), Apr. 2023, pp. 877–899.

[2] M. Bai, J. Yang, K. Pang, X. Xu, Z. Yang, and Y. Huang, “Provably robust and secure steganography in asymmetric resource scenario,” in Proc. IEEE Symp. Security Privacy (SP), May 2025, pp. 1438–1456.

[3] A. Cheddad, J. Condell, K. Curran, and P. Mc Kevitt, “Digital image steganography: Survey and analysis of current methods,” Signal Process., vol. 90, no. 3, pp. 727–752, Mar. 2010.

[4] B. Li, M. Wang, J. Huang, and X. Li, “A new cost function for spatial image steganography,” in Proc. IEEE Int. Conf. Image Process. (ICIP), Oct. 2014, pp. 4206–4210.

[5] F. Petitcolas, R. Anderson, and M. Kuhn, “Information hiding—A survey,” Proc. IEEE, vol. 87, no. 7, pp. 1062–1078, Jul. 1999.

[6] T. Pevny, T. Filler, and P. Bas, “Using high-dimensional image models´ to perform highly undetectable steganography,” in Proc. Int. Workshop Inf. Hiding, Jun. 2010, pp. 161–177.

[7] D. Huang, W. Luo, M. Liu, W. Tang, and J. Huang, “Steganography embedding cost learning with generative multi-adversarial network,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 15–29, 2024.

[8] Y. Zhang, Y. Ma, Q. Zhang, Y. Pei, and X. Luo, “An image robust batch steganography framework with minimum embedding signs,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 10745–10760, 2025.

[9] W. Lu, J. Zhang, X. Zhao, W. Zhang, and J. Huang, “Secure robust JPEG steganography based on AutoEncoder with adaptive BCH encoding,” IEEE Trans. Circuits Syst. Video Technol., vol. 31, no. 7, pp. 2909–2922, Jul. 2021.

[10] Y. Huang, Z. Liu, Q. Wu, and X. Liu, “Robust image steganography against JPEG compression based on DCT residual modulation,” Signal Process., vol. 219, Jun. 2024, Art. no. 109431.

[11] Y. Zhang, X. Luo, Y. Guo, C. Qin, and F. Liu, “Multiple robustness enhancements for image adaptive steganography in lossy channels,” IEEE Trans. Circuits Syst. Video Technol., vol. 30, no. 8, pp. 2750–2764, Aug. 2020.

[12] K. Zeng, K. Chen, W. Zhang, and Y. Wang, “Upward robust steganography based on overflow alleviation,” IEEE Trans. Multimedia, vol. 26, pp. 299–312, 2024.

[13] Z. Zhao, Q. Guan, H. Zhang, and X. Zhao, “Improving the robustness of adaptive steganographic algorithms based on transport channel matching,” IEEE Trans. Inf. Forensics Security, vol. 14, no. 7, pp. 1843–1856, Jul. 2019.

[14] Q. Liu, X. Xiang, J. Qin, Y. Tan, and Q. Zhang, “A robust coverless steganography scheme using camouflage image,” IEEE Trans. Circuits Syst. Video Technol., vol. 32, no. 6, pp. 4038–4051, Jun. 2022.

[15] L. Zou, J. Li, W. Wan, Q. M. J. Wu, and J. Sun, “Robust coverless image steganography based on neglected coverless image dataset construction,” IEEE Trans. Multimedia, vol. 25, pp. 5552–5564, 2023.

[16] B. Guo, P. Ping, and F. Xu, “Highly robust and diverse coverless image steganography against passive and active steganalysis,” IEEE Trans. Dependable Secure Comput., vol. 22, no. 3, pp. 2771–2787, May 2025.

[17] M. Yang, B. Qi, B. Ma, J. Xu, Y. Xian, and X. Li, “A highperformance region recognition network-enhanced deep CNN for image content perceptual hashing,” IEEE Internet Things J., vol. 12, no. 14, pp. 26456–26471, Jul. 2025.

[18] Y. Luo, J. Qin, X. Xiang, and Y. Tan, “Coverless image steganography based on multi-object recognition,” IEEE Trans. Circuits Syst. Video Technol., vol. 31, no. 7, pp. 2779–2791, Jul. 2021.

[19] J. Liu, L. Tan, Z. Zhou, W. Jiang, Y. Li, and P. Chen, “A dynamic YOLO-based sequence-matching model for eficient coverless image steganography,” Comput., Mater. Continua, vol. 81, no. 2, pp. 3221–3240, Nov. 2024.

[20] Y. Tan, X. Xiang, J. Qin, and Y. Tan, “Robust coverless image steganography based on human pose estimation,” Knowledge-Based Syst., vol. 296, Jul. 2024, Art. no. 111873.

[21] L. Meng, X. Jiang, Z. Zhang, Z. Li, and T. Sun, “A robust coverless image steganography based on an end-to-end hash generation model,” IEEE Trans. Circuits Syst. Video Technol., vol. 33, no. 7, pp. 3542–3558, Jul. 2023.

[22] X. Liu, Z. Ma, J. Ma, J. Zhang, G. Schaefer, and H. Fang, “Image disentanglement autoencoder for steganography without embedding,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Jun. 2022, pp. 2293–2302.

[23] Z. Yang, K. Chen, K. Zeng, W. Zhang, and N. Yu, “Provably secure robust image steganography,” IEEE Trans. Multimedia, vol. 26, pp. 5040–5053, 2024.

[24] W. Su, J. Ni, and Y. Sun, “StegaStyleGAN: Towards generic and practical generative image steganography,” in Proc. AAAI Conf. Artif. Intell., Mar. 2024, vol. 38, no. 1, pp. 240–248.

[25] X. Hu, S. Li, Q. Ying, W. Peng, X. Zhang, and Z. Qian, “Establishing robust generative image steganography via popular stable difusion,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 8094–8108, 2024.

[26] J. Yu, X. Zhang, Y. Xu, and J. Zhang, “CRoSS: Difusion model makes controllable, robust and secure image steganography,” in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), Sep. 2023, pp. 80730–80743.

[27] Y. Qi, K. Chen, N. Zhao, Z. Yang, and W. Zhang, “Provably secure image robust steganography via cross-modal error correction,” Proc. AAAI Conf. Artif. Intell., vol. 39, no. 25, pp. 26354–26362, Apr. 2025.

[28] Q. Zhou, P. Wei, Z. Qian, X. Zhang, and S. Li, “Improved generative steganography based on difusion model,” IEEE Trans. Circuits Syst. Video Technol., vol. 35, no. 7, pp. 6494–6507, Jul. 2025.

[29] W. Alexan, E. Mamdouh, A. Aboshousha, Y. S. Alsahafi, M. Gabr, and K. M. Hosny, “Stegocrypt: A robust tri-stage spatial steganography algorithm using TLM encryption and DNA coding for securing digital images,” IET Image Process., vol. 18, no. 13, pp. 4189–4206, Sep. 2024.

[30] K. Zeng, K. Chen, J. Zhang, W. Zhang, and N. Yu, “Toward secure and robust steganography for black-box generated images,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 3237–3250, Feb. 2024.

[31] Y. Zhang, X. Luo, C. Yang, D. Ye, and F. Liu, “A JPEG-compression resistant adaptive steganography based on relative relationship between DCT coeficients,” in Proc. 10th Int. Conf. Availability, Rel. Secur., Oct. 2015, pp. 461–466.

[32] Y. Zhang, X. Zhu, C. Qin, C. Yang, and X. Luo, “Dither modulation based adaptive steganography resisting JPEG compression and statistic detection,” Multimedia Tools Appl., vol. 77, no. 14, pp. 17913–17935, Jul. 2018.

[33] X. Yu, K. Chen, Y. Wang, W. Li, W. Zhang, and N. Yu, “Robust adaptive steganography based on generalized dither modulation and expanded embedding domain,” Signal Process., vol. 168, Mar. 2020, Art. no. 107343.

[34] Y. Zhang, X. Luo, X. Zhu, Z. Li, and A. G. Bors, “Enhancing reliability and eficiency for real-time robust adaptive steganography using cyclic redundancy check codes,” J. Real-Time Image Process., vol. 17, no. 1, pp. 115–123, Feb. 2020.

[35] M. J. Swain and D. H. Ballard, “Color indexing,” Int. J. Comput. Vis., vol. 7, no. 1, pp. 11–32, Nov. 1991.

[36] D. G. Lowe, “Distinctive image features from scale-invariant keypoints,” Int. J. Comput. Vis., vol. 60, no. 2, pp. 91–110, Nov. 2004.

[37] Y. Ma, L. Xu, Q. Zhang, Y. Zhang, X. Xin, and X. Luo, “EIS-OBEA: Enhanced image steganalysis via opposition-based evolutionary algorithm,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 3616–3631, Mar. 2025.

[38] Z. Tang, X. Zhang, and S. Zhang, “Robust perceptual image hashing based on ring partition and NMF,” IEEE Trans. Knowl. Data Eng., vol. 26, no. 3, pp. 711–724, Mar. 2014.

[39] I. Goodfellow et al., “Generative adversarial networks,” Commun. ACM, vol. 63, no. 11, pp. 139–144, Oct. 2020.

[40] J. Sohl-Dickstein, E. A. Weiss, N. Maheswaranathan, and S. Ganguli, “Deep unsupervised learning using nonequilibrium thermodynamics,” in Proc. Int. Conf. Mach. Learn., Jul. 2015, pp. 2256–2265.

[41] J. Ho, A. Jain, and P. Abbeel, “Denoising difusion probabilistic models,” in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), Dec. 2020, pp. 6840–6851.

[42] J. Song, C. Meng, and S. Ermon, “Denoising difusion implicit models,” in Proc. Int. Conf. Learn. Represent. (ICLR), 2021, pp. 1–22.

[43] C. Xiao, S. Peng, L. Zhang, J. Wang, D. Ding, and J. Zhang, “A transformer-based adversarial network framework for steganography,” Expert Syst. Appl., vol. 269, Apr. 2025, Art. no. 126391.

[44] L. Mescheder, A. Geiger, and S. Nowozin, “Which training methods for GANs do actually converge?” in Proc. Int. Conf. Mach. Learn., Jul. 2018, pp. 3481–3490.

[45] Y. Peng, D. Hu, Y. Wang, K. Chen, G. Pei, and W. Zhang, “StegaDDPM: Generative image steganography based on denoising difusion probabilistic model,” in Proc. ACM Int. Conf. Multimed. (MM), Oct. 2023, pp. 7143–7151.

[46] P. Bas, T. Filler, and T. Pevny, “‘Break our steganographic system’: The´ ins and outs of organizing boss,” in Proc. Int. Conf. Inf. Hiding (IH), May 2011, pp. 59–70.

[47] V. Holub, J. Fridrich, and T. Denemark, “Universal distortion function for steganography in an arbitrary domain,” EURASIP J. Inf. Secur., vol. 2014, no. 1, pp. 1–13, Jan. 2014.

![](images/1f11615e75fc1500d2e07ca06e0c207815772b71376540d8e8b44cc16aa7b9e8.jpg)

Mingliang Zhang received the M.S. degree from Information Engineering University, Zhengzhou, China, in 2022, where he is currently pursuing the Ph.D. degree. His research interests include information hiding and multimedia security.

![](images/2e1826290eef949c0ce2967b8c5416aa461c40067b58ee46d36f65d6bb913e5b.jpg)

Yi Zhang received the B.S., M.S., and Ph.D. degrees from the State Key Laboratory of Mathematical Engineering and Advanced Computing, Zhengzhou, China, in 2014, 2017, and 2021, respectively. She is currently a Teacher with the Key Laboratory of Cyberspace Situation Awareness of Henan Province, Zhengzhou, China. Her research interests include information hiding and multimedia security.

![](images/8e3165cbb930cc26f6ef53c1e18fb525ba7ad968112a7a081eaf237fd0314d29.jpg)

Yanmei Liu received the B.S. degree from Zhengzhou University of Aeronautics, Zhengzhou, China, in 2007, and the M.S. degree from Chongqing University, Chongqing, China, in 2011. She is currently pursuing the Ph.D. degree with Information Engineering University, Zhengzhou, China. Her research interests include multimedia security and image robust steganography.

![](images/cefd79b08a6cf9476a706fc252691fdf7a331861404a3dc408227b6bf4ce31b6.jpg)

Wentong Fan received the M.S. degree from Information Engineering University, Zhengzhou, China, in 2023, where he is currently pursuing the Ph.D. degree. His research interests include face reenactment and multimedia security.

![](images/e82359c4063e1a30f81cd9f9dc5de42272f49e5b71e3ec41a8b73bfc4e83688c.jpg)

Xiangyang Luo received the B.S., M.S., and Ph.D. degrees from the State Key Laboratory of Mathematical Engineering and Advanced Computing, Zhengzhou, China, in 2001, 2004, and 2010, respectively. He is the author or co-author of more than 150 refereed international journals and conference papers. He is currently a Professor with Henan Key Laboratory of Cyberspace Situation Awareness. His research interests include image steganography and steganalysis techniques.