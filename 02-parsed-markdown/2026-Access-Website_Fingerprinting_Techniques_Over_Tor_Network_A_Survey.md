Received 17 March 2026, accepted 3 April 2026, date of publication 7 April 2026, date of current version 16 April 2026. Digital Object Identifier 10.1109/ACCESS.2026.3681766

SURVEY

# Website Fingerprinting Techniques Over Tor Network: A Survey

FAISAL MURAD <sup>1</sup>, DEPENG CHEN<sup>1,2</sup>, ROLANDO TRUJILLO-RASUA<sup>2</sup>, AND MUHAMMAD ALAMGEER KHAN <sup>3</sup>

<sup>1</sup>School of Computer Science and Technology, Anhui University, Hefei 230601, China <sup>2</sup>Department of Computer Sciences and Mathematics, Rovira i Virgili University, 43007 Tarragona, Spain <sup>3</sup>Department of Automation, University of Science and Technology of China, Hefei 230000, China

Corresponding author: Depeng Chen (depengchen@ahu.edu.cn)

This work was supported in part by the University Synergy Innovation Program of Anhui Province under Project GXXT-2022–049, and in part by the Key Project of Anhui Provincial Department of Education under Project 2022AH050075. The work of Depeng Chen was supported by the Project HERMES funded by INCIBE and EU’s NextGenerationEU/PRTR. The work of Rolando Trujillo-Rasua was supported in part by the Ramón y Cajal grant under Grant RYC2020-028954-I, in part by the Spanish Ministry of Science and Innovation, in part by the EU, as well as by Projects PROVTOPIA under Grant PID2023-150098OB-I00, and in part by MICIU/AEI/10.13039/501100011033 and FEDER (EU), and HERMES, funded by INCIBE and the EU’s NextGenerationEU/PRTR.

ABSTRACT The increasing reliance on the Tor network for privacy has heightened the salience, potential impact, and adversarial incentives associated with Website Fingerprinting (WF) attacks. Although Tor employs layered encryption to protect content confidentiality and conceal endpoints, WF remains feasible because encrypted Tor traffic still exposes measurable side-channel metadata, most notably packet directionality, size-related effects, and timing characteristics, that can be exploited to infer user activity. For instance, while an observer cannot access payload contents, the temporal structure and direction of encrypted packet bursts observed during page retrieval can yield discriminative signatures that enable a statistical or learning-based classifier to differentiate among candidate websites or onion services. This paper presents a comprehensive survey of contemporary WF attacks on the Tor network, particularly focusing on advancements since 2019. We introduce a novel multi-level taxonomy that categorizes fingerprinting techniques based on their features, methodologies (including machine learning, deep learning, and hybrid approaches), and targeted components. Our analysis reveals that recent methodologies, especially those leveraging deep learning, have significantly enhanced attack accuracy and robustness, pushing the boundaries of de-anonymization in complex scenarios like multi-tab browsing. Furthermore, we highlight critical dataset and methodological gaps in current research, emphasizing the widespread reliance on simulated environments and synthetic data due to the inherent challenges of collecting real-world Tor traffic. By systematically examining existing limitations, we identify key open questions and provide concrete recommendations for future research, including the development of comprehensive datasets and standardized benchmarks, to foster more effective defense mechanisms and strengthen privacy within the Tor network.

INDEX TERMS Tor, website fingerprinting, deanonymization.

## I. INTRODUCTION

In the modern world, the Internet and digital technologies have become essential to daily life, facilitating the exchange of vast amounts of data. As technology continues to evolve, the sharing of sensitive information through digital channels has become increasingly common, creating significant privacy risks. In this context, Tor (The Onion Router) [1] has

The associate editor coordinating the review of this manuscript and iD approving it for publication was Zijian Zhang

provided a solution to millions of users worldwide [11], who use Tor to hide their traffic under various layers of encryption, each handled by a different relay node. At present, Tor operates with the support of over 6,000 relay nodes [2] through which users can access web services without the risk of being targeted, arrested, or censored [1], [3].

Although Tor is attractive for individuals with privacy concerns, it makes it harder for law enforcement agencies to combat illegal activities hidden behind Tor services, such as drug trafficking, human trafficking, and the dissemination of false information [4], [5]. Tor’s anonymity claims, therefore, have been under scrutiny for a long time. In particular, recognizing the difficulty of compromising relay nodes in Tor, a recent wave of attacks has focused on exploiting traffic metadata to identify and monitor users’ activities [6], [7], [8], [9]. In general, this type of attack is known as Website Fingerprinting (WF). The focus of this paper is to survey the characteristics of WF.

WF attacks primarily involve monitoring Tor traffic in real time, enabling eavesdroppers to surveil Tor users. Due to the properties of onion encryption, directly de-anonymizing a user’s online activity is challenging. WF attacks, instead, exploit patterns in Tor traffic, including those arising from misuse by certain users [13], [14]. A question that remains open is how effective WF attacks really are, and whether they can be deployed at a scale. While individual WF attacks claim high accuracy scores, their security assumptions might be too strong or their evaluation benchmark too narrow.

In this paper, we provide an in-depth synthesis of current research on fingerprinting attacks on the Tor network, focusing on the primary methods exploited and key findings from 29 papers, 18 of which were published after 2019. These recent contributions are not covered in previous surveys, making our work distinct due to its comprehensive approach to the topic. Our main contribution is the introduction of a multi-level taxonomy framework that categorizes fingerprinting techniques based on their methodologies. This includes key features, data collection methods, main tasks, and classifications of techniques such as machine learning, deep learning, and hybrid approaches. This taxonomy offers a systematic method for understanding and analyzing fingerprinting techniques, addressing a significant gap in the current literature.

We observed that new developments, particularly the usage of deep learning-based approaches, semi-supervised learning, and continual adaptation has to a great extent, improved website fingerprinting on Tor. Techniques such as Deep Nearest Neighbor Fingerprinting (DNNF) [34] and multi-tab fingerprinting framework e.g ARES [31], can achieve better results in complex and multi-tab browsing conditions. CoMask [77], on the other hand, introduces semi-supervised objectives like Masked Sequence Prediction (MSP) and Supervised Contrastive Learning (SCL) to improve generalization under evolving traffic patterns. FMWF [78] further extends WF to realistic overlapping multi-tab traces using synthetic data generation and few-shot transfer learning, while EIL-WF [79] focuses on efficient incremental adaptation to new sites through drift and imbalance. Real-world evaluations on onion services confirmed that WF remains practical, revealing that V3 services exhibit high fingerprints [80]. Recent studies such as CoDA [81] and COUNTMAMBA [82] address cross-domain shift and robustness in early stages, for predicting defense, and multi-tab identification. The overall results, however, expose the vulnerabilities and persistent weakness in Tor’s defenses, especially in more complex scenarios like multi-tab browsing.

Research areas for future investigation include developing adaptive defense mechanisms that can dynamically respond to evolving fingerprinting techniques. Another focus should be on enhancing the long-term effectiveness of defenses. Additionally, addressing the limitations of fingerprinting in real-world scenarios, such as multi-tab browsing and concept drift, is essential. Lastly, research should also focus on improving the data efficiency of WF attacks.

This paper makes several key contributions, particularly focusing on fingerprinting attacks on the Tor network:

• We conducted an in-depth study of the Tor network and its hidden services, providing an analysis of how the network operates and a comprehensive review of fingerprinting techniques used against it.

• We reviewed 28 fingerprinting attacks on the Tor network published in the past 6 years, 18 of which were published after 2019 and have not been covered in prior surveys.

• We proposed a new multi-level taxonomy that categorizes the fingerprinting techniques used to de-anonymize the Tor network.

• We highlighted critical dataset and methodology gaps in the field, shedding light on overlooked areas in prior survey papers and identifying avenues for further investigation.

• We identified critical limitations in existing WF studies and outlined key directions for future research. Meanwhile, we emphasize the need for comprehensive datasets, standard benchmarks, and studies resolving real-world scenarios.

We organized the core review sections to give a clear taxonomy (feature representations → attack techniques → learning paradigms) and key evaluation dimensions (closed- vs. open-world, single- vs. multi-tab, defended vs. undefended traffic, and concept/time drift). We did paper-by-paper descriptions with comparative discussion that highlights common mechanisms, contrasts assumptions and threat models, and synthesizes trade-offs in accuracy, robustness, computational cost, and real-time feasibility. Finally, we added a summary and consolidated cross-paper comparisons into updated tables/figures to make trends and gaps explicit.

This paper thoroughly investigates WF techniques in a systematic manner, which are applied to the Tor network. Section I delineates the topic, its objectives, and the review methodology. The previous study’s existing literature review, its identified gaps and limitations, and the scope of our paper are compared with other papers in Section II. A comprehensive overview of the Tor network, its privacy and anonymity attributes, and the underpinning principles of WF are illustrated in Section III. Section IV presents a new taxonomy classifying WF techniques on the basis of their de-anonymization strategies. Section V provides the different website fingerprinting attacks on the Tor network, including their methodologies and their influence on user anonymity. The existing research identified gaps and limitations; the proposed key recommendations for addressing them are highlighted in Section VI. Lastly, Section VII outlines a summary of the main findings, their implications, and suggests future research direction.

## A. REVIEW METHODOLOGY

This survey followed a systematic, step-by-step methodology for collecting and analyzing articles related to Website Fingerprinting (WF) attacks on the Tor network. Figure 1 illustrates the data collection process for this survey.

We searched four major sources—Scopus, Science Direct, IEEE Xplore, and Google Scholar—for research on Tor assaults that had been published between 2019 and 2025. The examination was initially done using ‘‘Website Fingerprinting attacks over Tor’’. Although over 2,360 records were shown, where numbers of articles were gathered from scientific fields containing the words ‘Tor’‘attacks’ but it was not related to our main concern. In order to narrow down the search results, the amendments were made to incorporate the term of fingerprinting and Tor. The excessive information was removed, which included irrelevant data, in order to achieve the desired results, specific journals and conference articles were focused. In order to see the feasibility and conductivity, a thorough evaluation was conducted while taking a careful check on the title, abstract, and keywords, along with the conclusion. The matter of interest in this regard was the papers that targeted WF assaults and evaluated the attacking maneuvers as contrasting to defensive ones.

Additionally, as far as the connection of papers is concerned, 28 papers were used to contribute to the information about WF attacks on Tor after careful evaluation and analysis. In our work, we highlight, evaluate, and debate the distinctive and significant contributions made by each of these chosen papers. These papers address a lot of concerns regarding current techniques and trends in WF assaults on Tor within the time and space limits. They also point up current shortcomings and gaps and offer suggestions on how to resolve these problems in the future.

![](images/461045cb7b7db8182f5a08284a2e7add1cc75d4e82299f3f025641ea78a42c27.jpg)  
FIGURE 1. Data Collection process of the survey.

## II. RELATED WORK

The earliest survey on WF attacks was published in 2018 [17] with a focus on machine learning approaches for monitoring encrypted communications within the Tor network. This work presents a taxonomy that categorizes traffic classification by input data (circuit, flow, or packet features), classification methods (supervised, semi-supervised, and unsupervised), and outcomes (ranging from traffic clusters to fine-grained traffic details). The survey also addresses the challenges encountered in employing machine learning approaches to analyze encrypted Tor communication, such as the network’s complex anonymization protocol. The limitation of the survey by Aaminuddin et al. [17] is the lack of details on specific fingerprinting techniques, which we do provide in our survey.

As the focus shifts towards targeted attacks, Enrico et al. [75] examined a variety of Tor assaults, classifying them based on whether they target clients, servers, or the Tor network itself, as the emphasis moves toward targeted attacks. Less than ten client-focused instances are identified in their examination, which depends on a prior study by [76]. However, our study complements the current comprehension of client-side vulnerabilities by highlighting more than 20 such attacks. Enrico et al. also looked at network-based attacks, including denial-of-service (DoS) and bridge discovery attacks, as well as server-side assaults that mostly target de-anonymizing or degrading hidden services. While they emphasized multi-target strikes, they did not go into great detail on particular WF techniques, which is an intriguing and increasingly prevalent field of exploration.

Basyoni et al. [49] further categorize Tor breaches based to their threat profiles and offer an extensive assessment of various traffic analysis attacks, such as segmented assault and those that employ a global aggressor model. Examining the range of de-anonymization techniques and the potentially harmful circumstances in which they function is their primary focus. They categorized menaces into three groups: node compromise, entrance flow capture, and global competitors. Basyoni et al. [49] presented insights into the viability and ramifications of each assault type by correlating these models with Tor’s preliminary threat models. Even while their study thoroughly investigated eight de-anonymization approaches, they merely discussed website fingerprinting and undetected services assaults.

## A. GAPS IDENTIFIED IN OTHER SURVEYS PAPER

Broad investigations like [17], [75] typically fail to devote particular consideration to evolving sectors like website fingerprinting and how it influences user anonymity. These writings offer an increasingly holistic approach to violations such as machine learning-based segmentation and traffic classification. They fail to, however, disclose precise details regarding website fingerprinting (WF) and recent investigations on it. Real-time authentication was not supplied by Basyoni et al. [49], who predominantly evaluated speculative or modeled assaults. In addition, the consequence of the newest or sophisticated assaults on Tor—specifically those that use innovative machine learning strategies—is overlooked in their assessment. In addition, examining website fingerprinting operations in light of existing adversary models is noticeably sparse.

Our survey paper addresses these gaps by specifically concentrating on WF attacks and their impact on the Tor network. We not only examine advanced approaches, such as machine learning and deep learning techniques, but also provide insights into the practicality of these methods in real-time situations. It includes a thorough analysis of the methodologies, effectiveness, and limitations of various WF techniques. As a result, it serves as a valuable resource for researchers studying traffic analysis and privacy issues within the Tor network. Table 1 provides a comparative analysis of attacks on the Tor network, summarizing key publications and their contributions in terms of the number of attacks discussed and whether they focus on WF.

By concentrating on the WF violations and their implications on the Tor network, our review article fills in these empty gaps. In alongside evaluating novel techniques like machine learning and deep learning, we additionally supply perspectives on how useful these methods are in situations that are immediate. It presents an in-depth assessment of the procedures, accuracy, and shortcomings of multiple WF procedures. It is consequently an invaluable resource for academics delving into issues with confidentiality and traffic evaluation on the Tor network. A comparative examination of Tor network assaults is given in Table 1, which also summarizes significant articles and their involvement with respect to the scope of attacks described and the manner in which they approach WF.

## III. BACKGROUND

This section provides an overview of the Tor network and its hidden services, explaining in detail how they operate. Meanwhile, it also includes a brief introduction to WF techniques to contextualize their significance within the Tor network.

## A. THE ONION ROUTER

Typically, Tor communication usually comprises three nodes(node 1 known as an entry node, node 2 known as a middle node, and node 3 known as an exit node) collectively form ‘‘Tor circuit’’. Messages are encrypted three times each, with each layer encrypted using a different key. As an encrypted message is transmitted through a circuit, it is decrypted by each node. One good aspect is that none of the three nodes possesses any knowledge of the source or the complete information about the message: the final destination is acquired by the exit node after decrypting the final layer. All of these intermediate three nodes are known as Onion Routers (OR), as the overall process imitates, like peeling off the layers of an onion. Tor leverages fixed-size cells of 512 bytes to maintain privacy and ensure security for transmitting data between the ORs [20]. Highlevel architecture of Tor is shown in Figure 2.

![](images/f690125fce86c7a465b1ec6770e9b3ad97cdc1619f4dd6c4d3cd767800c1b739.jpg)  
FIGURE 2. A simple schematic diagram of the Tor network. Users connect to the Internet through a sequence of onion routers, generally including an entry node, a middle node, and an exit node. Due to the open nature of the Internet, there is a potential for attackers to access specific routers within this network.

## B. HOW TOR WORKS

To fully understand Tor’s unique approach to protecting Internet privacy and ensuring anonymity, it’s crucial to grasp its internal mechanisms [1]. The Tor network operates as a relay network, where each (OR) functions as a user-level process without special privileges. Secure communication between ORs is maintained through TLS (Transport Layer Security) connections. The main components are as follows:

## 1) USER CONNECTION

To securely access the Tor network, the user uses strong local software called Onion Proxy (OP). The tool exploited by the user is not only unable to retrieve the directories and create the circuits, but it also allows numerous users’ connections to be handled. It enables the acceptance of the incoming TCP stream; once this stream is received, it effectively multiplexes them over the established circuits. In this way, OP ensures that the received data is transmitted to the destinations without any harm and is seamlessly relayed back by the OR on the other end, offer user a reliable browsing experience.

## 2) KEY MANAGEMENT

The Tor network has developed a strong key management system, which enables a smooth and Secure communication between the connected users. It provides a long-term identification key (K ) to each OR to sign different TLS certificates, descriptors for the router, and directories, offering authentication to the communication and observers whether it is coming from a legitimate source. For circui setup, the setup requests are decrypted using a short-term onion key and ephemeral session keys $( K _ { \mathrm { S e s s i o n } } )$ , calculated at each hop only, and are valid for the circuit lifetime. Furthermore, a symmetric link key $( K _ { \mathrm { L i n k } } )$ is created through the TLS protocol of encrypted communication among ORs. To enhance security, the short-term keys $( K _ { 0 \mathrm { { n i o n } } }$ and $K _ { \mathrm { L i n k } } )$ are rotated periodically, so that forward secrecy is satisfied, and the retrospective decryption is restricted in case of compromise. This separation of essential key roles and the periodic rotation of keys reduces the exposure and ensures the credibility of Tor’s anonymity promises.

TABLE 1. Comparative analysis of attacks on Tor.

<table><tr><td>Year</td><td>Publication</td><td>Main idea (Brief Overview)</td><td>Numbers of Attacks</td><td>WF Attacks</td></tr><tr><td>2018</td><td>Aminudinn et al. [17]</td><td>A survey: Tor encrypted traffic monitoring</td><td>Not given</td><td>Not</td></tr><tr><td>2019</td><td>Enrico et al. [75]</td><td>A survey: categorization of attacks on Tor</td><td>13</td><td>Not</td></tr><tr><td>2020</td><td>Basyoni et al. [49]</td><td>A survey: traffic analysis attacks on Tor</td><td>8</td><td>Not</td></tr><tr><td>2024</td><td>Our paper</td><td>A survey: fingerprinting techniques on Tor</td><td>28</td><td>Yes</td></tr></table>

## 3) CIRCUIT ESTABLISHMENT

A standard circuit of Tor comprises three nodes: an entry node, a middle node, and an exit node. When the client, via the OP, connects to a designated entry node and initiates a circuit, the process of circuit formation commences a TLS connection in order to establish a secure communication channel.

## 4) DATA TRANSMISSION

The client sends encrypted information via the entry node to a middle node serving as an intermediary. The middle node is clueless about the identity of the client or the data of the final destination.

## 5) SECURE EXTENSIONS

A TLS session is established between the client and the middle node for transmitting the messages via the entry node. The circuits extend to include the exit node when the symmetric key encryption is agreed upon. All this exchange of information involves multiple encryption in order to make sure of secure communication at each stage.

## 6) FINAL HOP AND DATA RELAY

The user has separate symmetric TLS keys with each node after the completion of the final hop of an established circuit. These multi-layered of encryptions not only allow the Tor circuit to securely send data and receive data but also enable it to maintain anonymity. Figure 3 illustrates the entire process.

## C. HOW HIDDEN SERVICES WORK

Hidden services are a key feature of Tor, allowing users to access websites anonymously by concealing the identities and locations of both the requester and the provider [21]. These services support various applications, such as websites and SSH servers, while ensuring that the server’s IP address remains hidden from the client [22], [23]. This anonymity is achieved by routing all communication through a Rendezvous Point (RP) that connects anonymous circuits between the client and the server.

Since 2004, Tor has incorporated hidden services to provide enhanced anonymity. When operating a hidden service, both the client’s IP address and the server’s location are kept confidential. The entire process of how hidden services work is illustrated in Figure 4 and summarized in the following steps:

![](images/2de6b5c83f673fb356f873a7f443340f377cddf45d51cfcf4c2190cc5ed7cc75.jpg)  
FIGURE 3. A simplified diagram illustrating Tor’s mechanism. The user initiates the process by creating a circuit with multiple layers of encryption using distinct keys, represented as $\{ \{ \{ m \} _ { k _ { 1 } } \} _ { k _ { 2 } } \} _ { k _ { 3 } } ,$ where m is the message and $\lbrace m \rbrace _ { k }$ denotes the encryption of m with key k. The message is directed through a series of selected onion routers, with each router decrypting a single layer and revealing the address of the subsequent hop. This process continues until the exit node, which transmits the encrypted message as TLS traffic to its intended destination. Each arrow in the diagram represents the peeling off of the corresponding key.

Step 1: The server selects three introduction points (IPs) by default and establishes circuits to them.

Step 2: The server generates a descriptor file containing its public key and information about the introduction points, and then uploads this onion service descriptor to a directory.

Step 3: The client obtains the ‘‘.onion’’ address and retrieves the service descriptor from the directory.

Step 4: The client selects a node to serve as the rendezvous point (RP) and requests the server to connect to this point.

Step 5: The client encrypts the RP information with the server’s public key and sends it to one of the introduction points. After verifying the request, the server receives the encrypted information and establishes a connection to the RP.

Step 6: The client and server can now securely exchange data through the rendezvous point.

## D. WEBSITE FINGERPRINTING

Website fingerprinting (WF) is a traffic analysis technique that analyses network traffic to extract meaningful information that Tor intends to hide. First introduced by Panchenko et al. [13], WF aims to classify the web pages visited by users on the Tor network, despite their traffic being encrypted [24], [25], [26], [28]. In a WF attack, local eavesdroppers monitor encrypted traffic, like the traffic used in tools such as Tor (for anonymous web browsing) or SSH (for secure remote connections), to infer which websites are being accessed.

![](images/07e5aaa39a25e4b2fe8534caee49efb746b8b475bcb26e38749e59d7edb8a936.jpg)  
(a) Establishing a circuit

![](images/879977b3fb2984834643f783f9c38f84ff750c87a609e9f1e7a895f2a1a2d714.jpg)  
(b) Generating descriptor file

![](images/1af6e7e01436ad7aa30aa830d17bd8c94c3156ff7c65d48b2fb0ba89fcdff334.jpg)  
(c) Fetching descriptor file from directory

![](images/ee69c75d6a4ef73195f989c6d11647ece57a774693a2e23c00ace04b570d63d5.jpg)  
(d) Client requests the server to connect at RP

![](images/22811404808bc32014a7da7103d0b0d0e31d624375bcac8e8a4f7c12f5cf9ae9.jpg)  
(e) Server connects with the RP

![](images/3ef00ab1c094079917c86c7b47b3734437d17c3e7f37da77e1510343c884017c.jpg)  
(f) Client and server exchange information through RP  
FIGURE 4. Six-panel figure illustrating the overall workflow: (a) establishing a circuit, (b) generating a descriptor file, (c) fetching a descriptor file, (d) client requests a connection, (e) server connects with RP, and (f) client–server exchange through RP.

At first, the Tor network was deemed to be impenetrable to WF attacks [13], [14]. This is due to the circumstance that Tor interceptors are limited to monitoring the direction and timing of encrypted Tor segments, which carry a fixed size of 512 bytes. However, by constructing counterfeit settings that closely replicate the networking circumstances of their desired recipients, eavesdroppers discovered ways to get through such constraints. In these configurations, they leverage the operational Tor infrastructure to routinely visit specific websites in an effort to obtain information regarding traffic. A supervised classifier that could recognize unique traffic trends associated with multiple webpages can be taught using this data. After having undergone training, the model may be used to identify the internet pages that individuals are visiting and examine network traces in real time.

WF attacks are usually divided into two categories based on the supposed outcomes:closed-world and open-world scenarios. This classification is done to effectively evaluate expected events. [27], [28].

## 1) CLOSED-WORLD SCENARIO

In this setup, the assailant constrains the handler’s admittance to a predefined set of websites and then endeavors to ascertain which particular site within this set the operator visits. For instance, the attacker might observe traffic structures from 200 websites and restrict the user’s access exclusively to these. Whereas this setup allows for controlled testing of WF techniques, it is generally impractical in real-world contexts. The implementation of such constraints is only possible in a well-structured and simplified network, which requires significant control over the user’s environment. Consequently, the closed-world scenario serves primarily as a theoretical or experimental model to assess the upper limits of WF attack accuracy.

## 2) OPEN-WORLD SCENARIO

In an open-world scenario, the user has the autonomy to access any website, while the observer aims to regulate whether a visited website fits a predefined and monitored set. If the visited website is a fragment of this set, the invader then tries to ascertain the specific website retrieved by the user.

To execute a traffic analysis attack, an attacker passively observes the activities of a user on the Tor network and collects the data shared between the server and the user. This gathered information helps the attacker to analyze the traffic patterns and predict websites that the user might visit. An open-world scenario allows users to do free browsing, providing ways through which the effectiveness of these traffic analysis attacks as compared to a closed-world scenario.

The attackers observe this anonymous network fragment, illustrated by a red line, to discern traffic arrays. This eavesdropper could be anyone with the competency to access and investigate network traffic near the user’s connection point [29].

![](images/f4d0b06348a0ea5849b61572af549de0a58ff86d5a07847169db1dea3ab3eb8b.jpg)  
FIGURE 5. Illustration of an attacker in a website fingerprinting (WF) attack on Tor, where Alice monitors Bob’s traffic over a shared Wi-Fi network to infer visited web pages.

A simple example of a WF attack is shown in Figure 5, where Alice attempts to determine the web pages visited by Bob, a Tor user accessing free Wi-Fi at a public library. To carry out this attack, Alice needs to capture and analyze the network traffic between Bob and the entry node of the Tor network. This requires Alice to be connected to the same Wi-Fi network as Bob to observe and collect the browsing traffic.

Once Alice intercepts the network traffic, she carries out a pre-processing phase to eliminate the extraneous data, particularly inaccessible pages and redirects. She then derives important traffic features from the observed data and chooses the most relevant ones for classification. The predetermined collection of websites is utilized to train a classifier that is not tailored to any specific individual user. However, it accumulates overarching traffic patterns related to these websites. After classifier training, Alice then employed a network sniffing tool to capture all network packets from Bob’s device. These packets are then subsequently fed into the trained classifier. If the classifier observes the patterns that match the webpages accessed by Bob and correspond to the known traffic signatures of the training set, Alice is able to infer the web pages visited by Bob. This simplified example generalizes part of the complexity of executing a website fingerprinting attack against Tor but demonstrates the general procedure of such an attack. This simplified example distills part of the complexity of executing a website fingerprinting attack against Tor but demonstrates the overarching methodology of such an attack.

## IV. TAXONOMY OF FINGERPRINTING TECHNIQUES

In this section, we introduced a taxonomy created specifically to classify the fingerprinting techniques that address the Tor network. At the top level, attacks are defined by the motive of the eavesdropper, which constitutes the key differentiation among various fingerprinting techniques. At the middle level, these methods are further sub-categorized based on the targeted elements within the network. However, at the lowest level, attacks are classified in terms of methodology deployed, which differentiates between active and passive approaches.

## A. WHY THIS TAXONOMY?

This taxonomy emphasizes the systematic organization of WF attacks within the Tor network. A well-structured taxonomy of these attacks provides a clearer explanation of its scope and the various mechanisms used for website fingerprinting.

This classification serves as a helpful tool for understanding the various types of WF attacks on the Tor network. Having a clear classification system makes it easier to see the different methods used to target and identify users in more advanced WF attacks. By categorizing WF attacks based on their goals, the components they take advantage of, and the tactics implemented. This framework highlights how attackers manipulate network features to unveil the identities of its users.

The taxonomy suggests a well-thought-out framework for imminent research and contributes to categorizing the prevailing and emerging attack procedures. By configuring acquaintance in an efficient manner, it allows scholars to assign possessions meritoriously, pay devotion to high-risk areas, and can equate the occurrence methodically; as a result, it will contribute to fragmentary encroachments in seclusion fortification for Tor users.

## B. DIFFERENT TYPES OF FINGERPRINTING TECHNIQUES

Fingerprinting techniques help adversaries detect and monitor Tor users by examining their online network activities. These techniques can de-anonymize users by analyzing their traffic features, including packet sizes, timing, and sequence, to produce unique identifiers based on their behavior. Our survey focuses primarily on Website Fingerprinting, as summarized in Figure 6. WF techniques can be classified mainly on the basis of the features employed, the methodologies, and the machine learning model deployed.

## 1) CLASSIFICATION BASED ON FEATURES USED

This method studies and examines network traffic to constitute unique fingerprints for various websites, which reveals what sites a user is visiting and breaks their anonymity. Polyzos [50] demonstrate that attackers follow this approach for collecting network traces of various Tor users and deeply observe the characteristics like the order of packets, their sizes, and the timing between them. The supervised classifier is trained on the identified features, which enables the eavesdropper to match new traffic to the known circuit fingerprints and predict which Tor circuits are being used.

## 2) CLASSIFICATION BASED ON ATTACK TECHNIQUES

Fingerprinting attacks on the Tor network can be sketchily divided into two types: passive attacks and active attacks. This arrangement plays a decisive role as it illuminates the numerous attack approaches exploited by eavesdroppers, constructed on the enormousness of the edge with the traffic. Active attacks establish direct stimulus by obstructing the Tor user traffic or altering it in some way to extract obscured evidence. These attacks are especially hazardous because they exploit flaws in the Tor protocol itself. For illustration, Fu et al. [53] projected protocol-level attacks, in which an observer feigns discrete cubicles in the Tor course. By interrupting the admittance sentinel and exodus router, challengers have the facility to alter traffic data, leading to miscalculations in cell exposure due to encryption distractions. This permits them to match the source and terminus traffic, fundamentally connecting the user activity and penetrating their anonymity.

![](images/af921f497256a28e5c0493c71f87010d3dfb058ea7ac204ea2b4413f0ee47f3a.jpg)  
FIGURE 6. Taxonomy of the tor attacks.

In distinction, passive attacks understand and collect data without relying on user traffic. These attacks are particularly focused on scrutinizing configuration and metadata to obtain compelling evidence. Auer et al. [55] portrayed thoughtfulness to the potential for Tor circuits to be compromised by application-level conventions. Their analysis revealed that the eavesdroppers had access to specific routers that could eavesdrop on the data sent through particular types of traffic, such as HTTP, Simple Mail Transport Protocol (SMTP), or P2P file allocation. By analyzing these mark circuits, observers can foretell user behavior and conceivably de-anonymize the users.

## 3) CLASSIFICATION BASED ON MACHINE LEARNING MODELS

Machine learning models are frequently implemented to analyze traffic patterns and distinctions across applications. Petagna et al. [51] exhibited that Tor is susceptible to application fingerprinting using traditional classifiers like Support

Vector Machine (SVM), k-Nearest Neighbors (KNN), and Random Forest (RF), obtaining over 97% accuracy on mobile device platforms. Wang et al. [52] proposed a multi-level classification method to detect Tor traffic on both PCs and mobile platforms, attaining a 60% accuracy rate for mobile apps. These findings show that application classification becomes more complicated on mobile devices than on PCs because of their dynamic and heterogeneous usage patterns.

## C. SUMMARY

This multi-level taxonomy offers a detailed categorization of WF attacks on the Tor network and a comprehensive framework on the basis of motive, targeted components, and employed methodologies to fully understand how eavesdroppers breach anonymity. This taxonomy outlines the particular vulnerabilities of the Tor network, which facilitates the creation of defense strategies by categorizing these techniques. It also lay groundwork to carry out future research studies, allowing to compare the results systematically and advancements for Tor user privacy protection.

## V. FINGERPRINTING TECHNIQUES ON TOR NETWORKS

In this section, we reviewed fingerprinting techniques that are employed to de-anonymize Tor network-encrypted traffic. We offer a detailed discussion of the fingerprinting techniques and their application within the Tor network. A summary of these fingerprinting techniques is shown in Table 2, and Table 3 delineates the benchmark of these fingerprinting attacks, and system performance assessment metrics of these fingerprinting attacks are illustrated in Table 4.

## A. OVERVIEW OF WEBSITE FINGERPRINTING

In this section, we provide an in-depth exploration of WF techniques over the Tor network. WF aims to identify the specific websites accessed by a user, even when their communications are encrypted or anonymized through systems like Tor. Although Tor provides strong anonymity by routing traffic through multiple relay nodes to conceal the user’s identity, WF can still exploit side-channel information to bypass some of Tor’s protections.

The primary challenge of fingerprinting within Tor is its anonymous circuit design, which dynamically routes traffic through multiple encrypted relays to conceal the origin and destination of user requests. Directly breaching this circuit would compromise Tor’s security model, but it is generally impractical due to the strong encryption and network-wide distribution of Tor nodes. Instead, WF attacks analyze sidechannel information, metadata such as packet size, timing, and direction, that can be passively observed to infer patterns that reveal user activity [54].

Here, we will explain the reason and features that the Tor network can be deanonymized by WF. We can have a summary of the key features in the Tor network for WF include:

## 1) KEY FEATURES EXPLOITED IN TOR WEBSITE FINGERPRINTING

WF over Tor relies on several distinctive traffic characteristics that can indirectly reveal information about user activity. The main features exploited in WF attacks include:

## a: TOR CIRCUIT CHARACTERISTICS [70]

The multi-relay path that packets traverse creates identifiable timing patterns, which can indirectly reveal information about user activity. While the circuit is anonymous, the packet patterns generated by various websites remain somewhat unique, even after anonymization.

## b: PACKET LENGTH AND DIRECTION [56]

The size of packets and their direction (incoming vs. outgoing) can be distinctive for different websites. Certain websites may generate unique packet size distributions, allowing attackers to differentiate one site from another.

## c: TIMING WINDOWS

The packet timing, inter-packet transmission, as well as the request responses, show gaps and can reveal additional patterns [57]. Websites with distinct content or server response behavior display varying timing characteristics that WF models can exploit.

## d: BURSTS

are categorizations of packets borne in a prompt sequence, often charted by a brief recess. Evaluating burst size, period, and bearing (inbound vs. outbound) can provide significant evidence about user activity [58]. Different websites and applications exhibit unique burst patterns based on how data is requested and served. For example, Burst size and duration may vary between websites with heavy multimedia content and those that are text-based. Inter-Burst Time (time between bursts) and Directionality (balance of incoming vs. outgoing bursts) can also serve as distinctive markers for different sites. In Tor WF, burst features combined with packet size and timing patterns offer a stronger basis for identifying website traffic, even without decrypting content.

## e: IP PORT ACCESS POINTS

While Tor masks IP addresses, the access points used for entry and exit can still provide indirect clues when analyzed alongside other metadata features [59].

## 2) DATA COLLECTION FOR WEBSITE FINGERPRINTING

Collecting raw data for the WF is crucial, as it directly influences the analysis accuracy [61]. Attackers may use various data collection methods, including passively capturing traffic at entry or exit nodes or collecting metadata during observation of known user behavior. The success rate of fingerprinting attacks relies on the quality and accuracy of the raw data; hence, it is critical to have efficient data acquisition methods.

## 3) PRIMARY TASKS AND METHODOLOGIES IN WEBSITE FINGERPRINTING

There are several key tasks and methodologies required for performing website fingerprinting over the Tor network [64]:

## a: FEATURE EXTRACTION

WF is based on the extraction and selection of meaningful characteristics that explicitly distinguish websites. Packet length, packet timing, circuit characteristics, and web metadata are all extracted and processed cautiously with an aim of analysis.

## b: MACHINE LEARNING MODELS FOR CLASSIFICATION

WF classifiers are generally trained on a wide range of diverse machine learning algorithms, including the Deep Learning model, SVM, and the RF. Such models are trained and can be used to identify patterns within different samples of traffic, thereby enabling them to determine the websites visited by the anonymous users.

## c: DATASETS AND DATA AUGMENTATION

WF experiments demand quality datasets, which provide a model training and validation structure. Given the heterogeneity of the Tor network traffic, maximizing the dataset that contains a heterogeneous sample improves the robustness and generalization of the model.

## 4) CLASSIFICATION APPROACHES ON THE TOR NETWORKBASED ON FEATURE SELECTION

The two most common classification strategies to determine and analyze the Tor traffic patterns are hand-crafted feature engineering and deep learning-based methodologies.

## a: HAND-CRAFTED

features method utilizes domain knowledge to identify certain packet-level characteristics manually. Then those features are employed in models such as the RF and SVM, which are capable of interpreting feature-rich data. A more interpretable model can be achieved through hand-crafted features and may be effective when there is limited labeled data available.

## b: DEEP LEARNING-BASED METHODS

Deep learning models, including Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs), can autonomously identify complex structures and arrangements in Tor. In addition, the CNNs emphasize multi-dimensional connections between the packet sequences. On the other hand, RNNs, specifically Long Short-Term Memory (LSTM) networks, have the ability to manage the sequential data and can learn the patterns in the traffic flow effectively. Consequently, these approaches are resource-intensive and are considered suitable for Website Fingerprinting complex activities, where accuracy is of the ultimate prominence. WF on the Tor network simulates a prominent challenge to user privacy. By considering and establishing the features, WF processes can ultimately improve the user experience, along with a high percentage of correctness, and even on anonymous setups.

## B. FINGERPRINTING BASED ON MACHINE LEARNING METHODS

Machine learning (ML)-based WF methods have greatly improved the effectiveness of fingerprinting attacks, especially in networks like Tor. These methods combine traditional numerical analysis techniques with advanced ML algorithms to identify traffic patterns, de-anonymize users, and monitor their network activity. By utilizing features such as packet size, timing information, and sequence patterns, they create a comprehensive framework for analyzing and classifying network traffic.

## 1) NUMERICAL FEATURES AND ANALYSIS TECHNIQUES IN ML FINGERPRINTING

Numerical values such as packet sizes, timing, and arrangement figures form the foundational structures used in many ML-based fingerprinting attacks. These standards assist as low-level inputs to ML models, offering inimitable identifiers for constructing traffic fingerprints. While primary tactics rely on manual analysis or numerical methods, current works have assimilated these numerical features into refined machine learning pipelines.

Platzer et al. [46] established the efficiency of numerical traffic features in a powerful deanonymization attack targeting Tor concealed amenities. The techniques that they follow share features with statistical demonstration to evaluate the structures and transmission measures. It includes sending, receiving, or imparting packages to identify the hidden service and systematic routes. By putting a strong and careful emphasis on the alterations of time between sending and receiving packets, the technique separated identical fingerprints. Similarly, this technique achieved a de- anonymization fraction of 100% on live Tor networks, supervising up to 25,000 requests on a daily basis. This highlights and emphasizes the potential and possibility of statistical features of traffic in improving machine learning based attacks.

Similarly, Yoshiura and Koizumi [47] leverages packet number patterns and timing features to study and analyze the hidden services. They use guard nodes to capture packages and emphasizing on three second windows following the broadcast of SYN packets, which enables them to efficiently detect hidden services. Their method focused on statistical structures; the intuitions learned from these studies can also be utilized to further enhance feature engineering for machine learning classifiers to bridge the gap between statistical analysis and programmed procedure. This revolutionizes the overall action and also paves the way for future productivity.

Building on these foundational numerical and analytical insights, researchers have introduced various ML models to enhance traffic analysis and classification:

• Bit-FP Framework: Zou et al. [60] employed an RF classifier and trained it by utilizing variables like packet size and direction. This allowed them to effectively categorize Bitcoin traffic over the Tor network with an accuracy of 0.989% and a recall of 0.987%. Their proposed methodology demonstrated the paths in which numerical attributes can be utilized in machine learning pipelines in an efficient way. Figure 10 delineates the proposed threat model.

• Website Fingerprinting Attack (WFA) Framework: Mei et al. [63] proposed two-phase machine learning algorithms to effectively classify Tor traffic in open-world settings. Their proposed approach integrates the sequence-based numerical characteristics into machine learning models to overcome problems such as rate-based fallacy and boost the model performance to efficiently enhance the accuracy, specifically in access network conditions. Figure 11 shows their proposed threat model.

• Circuit Fingerprinting Attacks: Huang and Du [62] leverages various classifiers such as SVM,Extreme Gradient Boosting(XGBOOST), and RF to develop a unique model, efficiently separating circuits created by various clients from those formulated by onion services. Their proposed model has effectively achieved 99% of recall and precision on the basis of numerical characteristics of traffic.

## 2) DEEP LEARNING METHODS FOR ADVANCED FINGERPRINTING

Deep learning approaches have taken traffic fingerprinting further by learning directly from raw traffic data, removing the need for manual feature extraction. These methods handle complex patterns and overlapping traffic sequences that traditional ML techniques or manual analysis cannot easily manage.

• Multi-Tab Website Fingerprinting (MT-WFA): Wang et al. [73] presented a novel deep learning-based Website Fingerprinting Detection (WFD) model illustrated in Figure 12. They utilized their proposed approach by integrating trace localization and various website classification to perform simultaneous analysis of multi-tab browsing.

• Block Attention Profiling Model (BAPM): Guan et al. [43] introduced a new model named the BAPM model, illustrated in Figure 14; it works by accepting the raw data and executing the integrated multi-head attention mechanism to investigate the raw data and examines any overlapping traffic traces in it. Their proposed technique helps to detect distinct website labels without the need for pre-segmented traces, which provides flexibility and accuracy.

## 3) HYBRID APPROACHES: NUMERICAL FEATURES,

## ANALYSIS, AND MACHINE LEARNING

Some methods combine traditional analysis techniques with machine learning to bridge the gap between statistical simplicity and computational robustness. For instance:

TABLE 2. Summary of recent studies on website fingerprinting.

<table><tr><td>Year</td><td>Publication</td><td>Settings</td><td>Approaches</td><td>Claims</td></tr><tr><td>2024</td><td>Lyu et al. [67]</td><td>both</td><td>Task-adaptive Modulation Unit(TMU), Ridge regression</td><td>First application of feature alignment-based meta-learning to few-shot WF attacks.</td></tr><tr><td>2024</td><td>Xu et al. [68]</td><td>both</td><td>R-CNN</td><td>First WF attack modeling traffic overlap as object detection problem</td></tr><tr><td>2024</td><td>Kim et al. [65]</td><td>Closed World</td><td>CUMUL features, 125 features</td><td>Their WF attack Reduce the computation time</td></tr><tr><td>2024</td><td>Wang et al. [69]</td><td>Both</td><td>Compact Convolutional Transformer</td><td>Addresses the CNN-based attacks limitations</td></tr><tr><td>2024</td><td>Yin et al. [71]</td><td>Both</td><td>CCT Adaptation, Convolutional token extraction, sequence pooling</td><td>Their study addresses the issues of computational efficiency and feature extraction of Tor traffic analysis</td></tr><tr><td>2024</td><td>Mathews et al. [72]</td><td>Both</td><td>Multi-channel traffic representations, Transformer-based model architecture</td><td>Reducing the remaining anonymity in tor against Website fingerprinting</td></tr><tr><td>2024</td><td>Deng et al. [74]</td><td>Both</td><td>Temporal Distribution Analysis, Adaptive Data Augmentation, Spatial Distribution Analysis, Early-Stage Identification</td><td>First reliable WF attack outperform 9 baselines</td></tr><tr><td>2023</td><td>Bang et al. [30]</td><td>Closed world</td><td>Federated Learning (FL)</td><td>First study to apply FL to WF to deal with centralized approaches issues</td></tr><tr><td>2023</td><td>Deng et al. [31]</td><td>Both</td><td>Transformer Model</td><td>Design for multi-tab WF attack on multiple browsing setting</td></tr><tr><td>2023</td><td>Guo et al. [34]</td><td>Both</td><td>CNN, KNN</td><td>Obtained effective WF with few resources</td></tr><tr><td>2022</td><td>Wang et al. [32]</td><td>Open world</td><td>Deep Neural Network</td><td>Cover wide range of unmonitored websites, First study to achieve better performance under concept drive</td></tr><tr><td>2023</td><td>Pan et al. [33]</td><td>Both</td><td>CNN</td><td>Extraction of features from packet direction and time interval</td></tr><tr><td>2019</td><td>Jahani et al. [35]</td><td>Both</td><td>Fast Fourier Transform</td><td>Apply new online WF attack to existing WF limitation</td></tr><tr><td>2022</td><td>Sun et al. [36]</td><td>Both</td><td>Neural Networks</td><td>Extraction of direction and time length</td></tr></table>

• Triplet Fingerprinting (TF): Sirinum et al. [42] used N-shot learning to classify traffic with minimal training data, achieving 85% accuracy with only five samples per class.

• Hidden Service Response Fingerprinting: Meng and Fei [66] proposed a model to effectively improve the classification accuracy by utilizing the response time characteristics and numerical features shown in

TABLE 2. (Continued.) Summary of recent studies on website fingerprinting.

<table><tr><td>Year</td><td>Publication</td><td>Settings</td><td>Approaches</td><td>Claims</td></tr><tr><td>2023</td><td>Attarian et al. [37]</td><td>Closed world</td><td>CorrClassifier Model</td><td>Evaluated direction informationRemove unpredicted noises</td></tr><tr><td>2022</td><td>Wang et al. [38]</td><td>Closed world</td><td>Multi-similarity Model</td><td>Apply WF to anonymous network</td></tr><tr><td>2019</td><td>Tian et al. [40]</td><td>Both</td><td>Neural Network</td><td>Address scalability issues in WF attacks</td></tr><tr><td>2019</td><td>Lai et al. [41]</td><td>—</td><td>Wavelet Transform, SVM</td><td>WF for anonymous network</td></tr><tr><td>2021</td><td>Zou et al. [60]</td><td>Closed world</td><td>Random Decision tree</td><td>Identify Bitcoin services over Tor</td></tr><tr><td>2021</td><td>Hantao et al. [63]</td><td>Open world</td><td>Two-stage scheme</td><td>Web pages identificationAddress Base fallacy issues</td></tr><tr><td>2022</td><td>Huang et al. [62]</td><td>—</td><td>SVM, XGBoost, Random Forest</td><td>Discovering Onion services</td></tr><tr><td>2022</td><td>Wang et al. [73]</td><td>Real world</td><td>WFD Model</td><td>Reinvestigate multi-tab website fingerprinting issues</td></tr><tr><td>2020</td><td>Meng et al. [66]</td><td>Open world</td><td>Response Time Feature</td><td>WFP on Hidden services</td></tr><tr><td>2019</td><td>Sirinum et al. [42]</td><td>Open world</td><td>N-shot Learning</td><td>Boost WF attackFirst study to improve bootstrapping of models.</td></tr><tr><td>2021</td><td>Liu et al. [43]</td><td>Open world</td><td>Block attention profiling</td><td>Consider for multi tabs browsing</td></tr><tr><td>2019</td><td>Attarian et al. [44]</td><td>Both</td><td>Adaptive streamlining Algorithm</td><td>WF on anonymous network</td></tr><tr><td>2020</td><td>Platzer et al. [46]</td><td>closed world</td><td>Created own Tor client and hidden service</td><td>Independent methods to deanonymize any Hidden services</td></tr><tr><td>2020</td><td>Yoshiura et al. [47]</td><td>Open world</td><td>Relay nodes</td><td>Collecting hidden service IP addresses</td></tr></table>

Figure 13. They achieved higher accuracy as compared to traditional techniques such as K-NN and k-Fingerprint (k-FP).  
the specificity of traditional traffic analysis with the generalization power ofML models.

These examples highlight how numerical analysis and machine learning can complement one another, combining

## 4) SUMMARY

The simultaneous use of the numerical features, statistical analysis, and machine learning model has led to the emergence of a diverse range of fingerprinting techniques. Conventional methods primarily based on numerical values constitute the building blocks for feature engineering, whereas the machine learning and deep learning techniques enhance the practicality of these techniques, providing robust and scalable fingerprinting attacks. This synergy illustrates the evolution from simple traffic analysis to sophisticated, model-driven fingerprinting solutions.

## C. FINGERPRINTING BASED ON DEEP LEARNING ALGORITHMS

It has been observed that deep learning techniques are the most promising source for Website fingerprint attacks, especially when executed on the Tor network and analyzing the encrypted data. This allows them to figure out websites with greater accuracy and reliability. These models utilize side-channel information—such as packet size, timing, and traffic direction—collected during communication to infer user activity, even when anonymization techniques are used.

## 1) FEDERATED LEARNING FOR PRIVACY-PRESERVING WEBSITE FINGERPRINTING

To address privacy concerns and computational bottlenecks in centralized WF systems, Bang et al. [30] proposed a Federated Learning (FL) framework. This decentralized approach allows Tor nodes to train local models using their own datasets without sharing sensitive data. Key components of the framework include:

• Collaborative Model Training: The authors independently train local models at each node (client), and a global model aggregates knowledge from all nodes involved in training. Nodes, ensuring data privacy

• Feature Selection: Advanced methods alleviate data complexity, minimize training time while maximizing accuracy

• Efficient Node Management: Data-driven nodes and model retraining, preserve scalability and efficiency throughout the distributed system

By utilizing federated learning, this framework improves the WF model accuracy and addresses the issues of privacy concerns related to centralized data collection. Figure 7 illustrates the design of the FL framework.

## 2) ROBUST MULTI-TAB FINGERPRINTING WITH ARES

Multi-tab browsing complicates WF attacks, as users simultaneously access several websites, creating overlapping traffic patterns. Deng et al. [31] addressed this challenge with ARES (WF attack framework), a framework that frames WF as a multi-label classification problem. ARES employs:

Multi-Classifier Approach: Each classifier is trained to recognize traffic patterns specific to a single website, enabling accurate identification of multiple websites accessed in parallel.

• Transformer Model: By utilizing a novel transformer architecture, specialized in processing local traffic patterns across distinct segments, which effectively differentiates individual sites in a complex browsing environment.

![](images/a28e8d42a379f28568b42885004c521693a504716420ced49afbf45a06f6bc9e.jpg)  
FIGURE 7. A federated learning deployment illustrating the distributed training of models across tor nodes without sharing local datasets, contributing to the creation of a global model while preserving privacy.

ARES is stated to be effective in handling multi-tab browsing and demonstrated high accuracy in real-world scenarios. Figure 8. shows the ARES framework.

![](images/0413c24347466911ee96aac4ee6b785e6a4d8459b86631b5251bf1020ce3bcd4.jpg)  
FIGURE 8. Threat model of the ARES framework for multi-tab website fingerprinting.

3) ADVANCES IN DEEP LEARNING-BASED WF ATTACKS Several advanced deep learning-based WF techniques have further enhanced attack capabilities:

• Deep Nearest Neighbor Fingerprinting (DNNF): Guo et al. [34] combined CNNs to extract features and a K-NN classifier to make predictions. DNNF can effectively deals and manage limited training data, and is acclimated to probability drift, achieving high accuracy with minimal samples.

• snWF (Neural Network Ensemble for WF): Wang et al. [32] presented snWF, which utilizes ensemble-based learning to minimize the variability of the model. This method is not only effective in open-world settings but also offers high robustness with low false-positive rates.

• Fine-Tuning CNN-Based WF (FM-CWFA): Pan et al. [33] presented FM-CWFA, which implements a fine-tuning mechanism that adjusts to changing traffic patterns. Their methods show robustness even with small training datasets and effectively achieve high accuracy in both open and closed world settings.

## 4) DEEP LEARNING METHODS FOR ADVANCED FINGERPRINTING

These methods excel at identifying overlapping traffic patterns that traditional approaches cannot manage:

• Block Attention Profiling Model (BAPM): Liu et al. [43] presented BAPM, which examines the overlapping traffic segments by leveraging both raw packet traces and a multi-head attention mechanism. This model offers flexibility and improved accuracy, and also predicts concurrent websites’ labels without presegmenting traces.

• Task-adaptive Feature Alignment Network for WF (TFAN): Lyu et.al [67] present TFAN by leveraging deep learning to design a meta-learning framework for few-shot website fingerprinting on TOR. The authors utilize ridge regression and a task-adaptive modulation unit in order to achieve efficient feature alignment and an improved discriminative channel weighting. TFAN attains an accuracy of 92.8% in a 1-shot setting while retaining an accuracy of more than 90% after 42 days, outperforming the state-ofthe-art like Triplet Fingerprinting (TF) and Transfer Learning Fingerprinting Attack (TLFA). The proposed attack efficiency and resilience make it a substantial advancement in real-time WF attacks, demonstrating the need for improved anonymity defenses.

• Trace Image-based Object Detection based for WF (TIOD) : Xu et al. [68] propose TIOD, which achieves over 85% accuracy in two tab settings, outperforming all existing models without requiring prior knowledge of tab counts or re-training for dynamic scenarios. Its resilience against overlapping traffic and ability to adapt to multi-tab settings make TIOD superior to conventional WF attacks, providing a novel and scalable solution for practical Tor traffic analysis.

• Compact Convolutional Transformer Website Fingerprinting (CTWF) attack: Lyu et al. [69] proposed a novel Model CTWF (Compact Convolutional Transformer), that tackles the issues of traditional deep learning models like CNNs, which are struggling to capture the long-term dependencies in traffic data, leading to limited effectiveness. The authors integrate a convolution token extraction layer and a sequence pooling layer into a transformer architecture to effectively improve the model efficiency and accuracy. Compared to the existing attack model, their model achieves notable classification accuracy of 99.42% under various conditions such as time drift and defense strategies in a closed world scenario.

• A Multi-tab Website Fingerprinting Attack Based on Fixed Dimensions for Tor Network: Yin et al. [71] proposed the FD-WF model to address critical gaps in website fingerprinting by introducing an innovative fixed-dimension approach for multi-tab and mixed-tab scenarios within the Tor network. The novel methodology of FD-WF addresses single-tab limitations by employing an optimized fixed dimension and an enhanced Res-Net, which resolves feature blurring in mixed traffic, ensuring resilient classification even when the number of tabs is unknown. FD-WF not only advances the WF research domain but also creates additional standardized benchmarks in the domain of privacy and security analysis of anonymous networks, filling the gap between theory and real-time practicality.

• LASERBEAK: Mathews et al. [72] present the LASERBREAK model, which leverages multi-level representation and transformer architecture against FRONT-defended traffic, achieving 96% of accuracy. It also shows an improvement of 36.2% compared to existing state-of-the-art models. Moreover, they offer a dataset of 500,000 samples, techniques of precision optimization, and crucial information on subpage fingerprinting, which exposes serious risks to anonymity. After deep investigation, the authors of [72] establish a new benchmark for WF attacks more efficient and highlight the need for more effective defensive mechanisms.

• Holmes: Deng et al. [74] propose an innovative early-stage WF assaults that can detect traffic of the Tor network with only 21.71% of a page load. Their proposed method achieved an average performance improvement of 169% on F1-score performance compared to the state-of-the-art attacks. Under dynamic conditions and countermeasures, Holmes effectively manages to correlate early-stage traffic with comprehensive traffic using adaptive data augmentation, temporalspatial distribution analysis, and supervised contrastive learning.

## 5) SUMMARY

The integration of deep learning into WF attacks has resulted in significant advancements, including federated learning frameworks, transformer-based models for multitab scenarios, and neural network ensembles. These innovations have notably enhanced the accuracy, scalability, and robustness of WF attacks, exposing the vulnerabilities of anonymization networks such as Tor. As these techniques advance, effective defense will necessitate sophisticated countermeasures, including improved traffic obfuscation and adversarial machine learning strategies.

## D. TRANSFORM-BASED METHODS

Transform-based approaches utilize mathematical principles to identify the patterns of network traffic and classify it. These kind of approaches offers an alternative to deep learning by concentrating on the extraction of features via domain-specific transformations, i.e., Fourier and wavelet transform. although transform based approaches are not as adaptive as deep learning, but offers more advantages, such as computational efficiency and interpretability. Overall, it makes them appropriate for the settings with limited resources or real-world processing requirements.

## 1) CORE TECHNIQUES IN TRANSFORM-BASED

## FINGERPRINTING

Transform-based methods rely on mathematical properties to extract features that reveal underlying traffic patterns. Key approaches include:

## a: FAST FOURIER TRANSFORM (FFT)

Jahani et al. [35] employed the Fast Fourier Transform approach to create an online website fingerprinting attack, effectively exposing the periodic patterns by translating the time domain traffic data into the frequency domain. They proposed two novel parameters in their model: symbol of class and the distinct vector of instance. They incorporate both novel parameter to an improved FFT algorithm to figure out the measurement of similarity distance, which enables them to effectively detect the observed websites correctly, even in noisy situations.

Building on advancements in the field, Sun et al. [36] proposed a novel approach for detecting Tor users who browse the web using Frequency Domain Fingerprinting (FDF). This technique leverages circuit sequences in the access traffic network to extract time and direction, and transforms this information into the frequency domain to examine Tor network traffic. They reached classification accuracies of 98.8% and 94.3% for the undefended and defensive settings, respectively, by integrating self-attention, CNNs, and FC layers.

## b: WAVELET TRANSFORM

Lai et al. [41] leverages the wavelet transform to disassemble network traffic into several frequency parts to facilitate high-level and in-depth analysis. They combined and utilized wavelet-based feature extraction with an SVM classifier, attaining an average accuracy of 96.7%. Their proposed method highlights the enhancement of wavelet analysis in distinguishing the uniqueness of traffic.

To address the issue of diverse device performance in WF, Wang et al. [38] introduced a cross-platform website fingerprinting attack with multi-similarity loss. They applied a multi-similarity model to differentiate anonymous website traffic and device-specific variances. Their approaches collect data from a single device to train a classifier, which enables it to effectively detect anonymous traffic across simultaneous platforms.

## 2) HYBRID TRANSFORM-BASED APPROACHES

Modern fingerprinting techniques are increasingly integrating transforms with machine learning. Some notable examples are

## a: FREQUENCY DOMAIN FINGERPRINTING (FDF)

introduced by Sun et al. [36].This hybrid framework combines frequency-domain analysis with neural networks.

It extracts features related to packet length and direction, transforms them into the frequency domain, and processes them using a model that incorporates self-attention, CNNs, and Fully Connected (FC) layers. This approach achieved classification accuracies of 98.8% for undefended Tor traffic and 94.3% for defended Tor traffic, demonstrating the effectiveness of combining transforms with learning-based classifiers.

## b: BURST CODING AND WAVELET DECOMPOSITION

Tian et al. [40] proposed ‘‘Tiny Website Fingerprinting’’, a lightweight method tailored to resource-constrained environments. By combining burst coding with wavelet decomposition, they reduced dimensionality while retaining critical traffic features. Tiny WF achieved a 90.5% success rate against Website Traffic Fingerprinting Protection with Adaptive (WTF-PAD) defense and a 98.2% top-2 accuracy against Walkie-Talkie defenses, highlighting its effectiveness in overcoming traffic obfuscation techniques. Their proposed model is illustrated in Figure 9.

## 3) ADVANTAGES AND LIMITATIONS

Transform-based methods offer several advantages:

• Computational Efficiency: These methods acquire fewer computational resources as compared to deep learning based models, which is suitable for lightweight or real-time applications.

• Interpretability: The explicit use of mathematical properties allows for easier understanding and debugging of the models.

• Versatility: Techniques like FFT and wavelet transforms are broadly applicable across various traffic scenarios.

However, these methods also face limitations:

• Sensitivity to Noise: Transform-based models can struggle with noisy or obfuscated traffic, as their reliance on fixed features makes them less adaptive.

• Lower Scalability: Unlike deep learning, these methods are less effective in handling large-scale, complex datasets.

• Restricted Adaptability: They may underperform when traffic patterns evolve, requiring manual updates to remain effective.

## 4) PRACTICAL IMPLICATIONS AND FEASIBILITY

Transform-based techniques are arguably not as powerful as deep learning; nevertheless, there are still some transform-based applications that remain viable in practice. As an example, in resource-limited scenarios, where the main concern is computation overhead, such techniques provide a feasible alternative. Hybrid approaches show promising results in balancing efficiency and accuracy by integrating transforms-based method with machine learning techniques such as (FDF and Tiny WF). Nevertheless, implementation of such techniques in real-life applications, one should take into account their vulnerabilities to noise and low scalability.

![](images/d377700d9cf502ebd0eca8dba02a0e6704d9cc438b3578acd875159b5e587e41.jpg)  
FIGURE 9. The threat model of tiny website fingerprinting attack.

![](images/5f885e8079e8cadaba9751ad8e66e0eaab6ba7ce1e7aeb896dab7f9734fcb449.jpg)  
FIGURE 10. The attacker observes the bitcoin nodes via Tor hidden services by executing a traffic fingerprinting attack, which allows an adversary to exploit distinct traffic patterns to identify and track user activities.

![](images/c2e7b587afa73844f72c28050b9391127d89f67fa5ea230e22e27ae76bfb4f47.jpg)  
FIGURE 11. WF is applied on core gateways to monitor a large amount of traffic, rather than on access gateways.

## E. OBSERVATION

After the analysis of the literature on WF techniques over the Tor network has yielded several essential insights. These observations highlight the recent trends, gaps, and challenges, and offer a foundation for future work. Below are the key findings drawn from the analysis of the literature:

1) Emerging Trends: The latest development in the WF techniques has been enhanced by the integration of deep learning techniques, such as federated learning through an optimized traffic analysis process for de-anonymizing users privacy in the Tor network.

![](images/a11e01f5b207934972aa3651cd19c9328aba3c7085045b4c475339814fe465e9.jpg)  
FIGURE 12. Adversary operates guard-flagged onion routers in Tor, passively recording traffic without altering it.

![](images/14d1be8f17f03577070d419551506f0607dee83d19ab2682b6bc3576d80e2966.jpg)  
FIGURE 13. Hidden services response fingerprinting attack,local attacker infer hidden service content by analyzing the response time of encrypted traffic.

![](images/21e2d4609e1d56d8ef6760835bef8aff18a706a5236a8a48e47bd0b0fcc1169d.jpg)  
FIGURE 14. BAPM:The multi-tab WF attack process, where an attacker is analyzing the directional sequences of network traffic by training a classifier using packet traces to infer visited websites.

2) Research Gaps: The current literature indicates that limited comprehensive studies are focusing on WF attacks across various scenarios, especially in contexts involving multiple users in different environments. Furthermore, there are some gaps that remain unaddressed in the literature about the successive browsing behaviors and their impact on the success rate of WF attacks.

3) Methodological Advancements: Innovative techniques, including adaptive online WF attacks that use stream mining algorithms and a robust multi-tab WF attack model, have significantly advanced the management of complex browsing patterns and the ability to adapt to real-time changes in network conditions.

4) Conflicting findings: The varying numbers of success rates of WF approaches with an increased number of tabs and users demonstrate that the applicability of these techniques may fluctuate under certain conditions; therefore, there is a need for a more optimized solution.

5) Key Challenges: A significant issue identified is the challenge of precisely fingerprinting individual behaviors, particularly when users view numerous tabs or consecutive webpages, complicating the de-anonymization process.

6) Future work: The development of new datasets to incorporate a wider range of system configurations and developing robust countermeasures against WF attacks in multi-tab environments represents possibilities for future work in this field.

## VI. LIMITATION AND RECOMMENDATION

Based on the discussion in Section V, which focuses on fingerprinting techniques over the Tor network, it is evident that WF poses significant challenges to privacy and anonymity. While WF has been shown to be a potential method for de-anonymizing Tor users, its effectiveness and applicability in real-world scenarios are limited by several key issues. These limitations obstruct the widespread adoption of WF in Tor’s encrypted network.We have identified and organized these limitations and associated gaps in Table 5.

## A. LACK OF EMPIRICAL DATA FROM REAL-LIFE TOR USERS

Although there are various novel techniques proposed to enhance the ability of WF over the Tor network, one significant limitation is the absence of an empirical dataset from real-life Tor users. Collecting data from real Tor users risks exposing sensitive information, which violates the fundamental principle of user privacy that Tor is designed to protect. However, without access to real-world traffic, researchers often have to rely on simulations that may not accurately represent the diversity and complexity of real Tor traffic. In that case, the attack performance on a real application might not be that significant compared to the researcher’s statement.

## B. THE SHORTCOMINGS OF EMULATING TOR NETWORKS

To address the privacy concerns, some researchers resort to emulating the Tor network on a small scale to gather data. However, this approach has three significant limitations.

First, simulated networks lack the complexity of the real Tor network, such as diverse relay configurations, varying latency strategies, and real-world traffic patterns. Second, the variety of user behavior, browsing settings, and plugins in real-world scenarios can hardly be fully replicated in a controlled environment. And this leads to a potential overestimation or underestimation of WF effectiveness. Last but not least, small-scale emulations cannot replicate the massive scale of the Tor network, which may impact the generalization of the findings.

## C. RELIANCE ON THE SYNTHETIC DATA

Other studies resolve the lack of real-world data by exploiting the synthetic datasets generated from pre-defined models of user behavior and network traffic. While synthetic data offers a controlled and privacy-preserving alternative, it also introduces several shortcomings. First, synthetic datasets often rely on assumptions about Tor traffic patterns, user behavior, and Tor relay performance, which may not hold true in practice. Second, the noise, variations, and anomalies in real-world traffic are often hard to simulate, which potentially leads to an oversimplified view of the WF attack success rate. Last, the design of synthetic datasets may inadvertently introduce bias, making them less representative of real-world conditions.

## D. ABSENCE OF BENCHMARK FOR WF EVALUATION

As a consequence of the limitations of both emulated networks and synthetic datasets, there is currently no universally accepted benchmark for evaluating WF attacks. This lack of standards creates several challenges. First, it becomes more difficult to compare the performance of different WF attacks across studies. Second, without a benchmark dataset or framework, it becomes challenging to reproduce results and validate claims in the literature. Lastly, it’s hard to capture the true effectiveness of WF attacks in practical settings.

## E. THE OPEN QUESTIONS AND CHALLENGES

## 1) OPEN QUESTIONS

One of the critical open questions in website fingerprinting (WF) research is how to effectively pre-process Tor traffic for implementation in real-world scenarios. This challenge arises due to various factors that introduce variability into traffic characteristics.

First, different browsers contribute unique attributes to traffic, such as variations in packet sizes, timing patterns, and HTTP headers. These browser-specific features complicate the standardization of WF methods. Second, plugins, extensions, and user settings (e.g., enabling or disabling JavaScript, privacy-focused configurations) can significantly alter traffic patterns, creating additional layers of complexity. Lastly, user behaviors and browsing context—such as the number of open tabs, types of visited websites, and specific interactions like streaming video or downloading files—also influence the traffic data available for fingerprinting.

TABLE 3. Benchmark of WF.

<table><tr><td>Algorithms</td><td>Dataset</td><td>Accuracy</td><td>False Positives</td><td>AUC (Concept Drift)</td><td>Methodologies</td></tr><tr><td>Federated Learning [30]</td><td>DF dataset</td><td>95%</td><td>2.5%</td><td>Not reported</td><td>Uses FL with feature selection and adaptive node selection to balance privacy, training time, and accuracy.</td></tr><tr><td>ARES [31]</td><td>Real-world multi-tab Tor sessions</td><td>91.3%</td><td>5%</td><td>AUC initial stage: 100%; AUC after 30 days: 85.1%; Performance drop after 30 days: 14.9%</td><td>Uses multi-label classification with Trans-WF for local traffic pattern analysis and multi-classifier approach to identify visited websites.</td></tr><tr><td>DNNF [34]</td><td>AWF 100, AWF 775, AWF 200, Wang 100</td><td>96.2%</td><td>1.5%</td><td>AUC initial stage: 90%; Performance drop after 30 days: 3%; AUC after 60 days: 87%</td><td>Combines CNN for feature extraction with k-NN for classification, optimized for small sample sizes and robustness to concept drift.</td></tr><tr><td>snWF [32]</td><td>C0, W0, Concept Drift</td><td>91%</td><td>5.7%</td><td>AUC initial stage: 86%; AUC after 30 days: 67%</td><td>Neural network ensemble method using snapshot ensemble deep learning to improve robustness against concept drift and imbalanced data.</td></tr><tr><td>CWFA [33]</td><td>Undefended DF, Defended DF, Undefended Wang, Defended Wang</td><td>99%</td><td>7%</td><td>AUC initial stage: 96%; AUC after 30 days: 79%</td><td>Uses CNN-based transfer learning, integrating packet direction and timing sequences for effective classification under concept drift.</td></tr><tr><td>FFT [35]</td><td>DSD-2, DSD-4, DSD-6, DSD-8, DSD32, DSD64</td><td>98.48%</td><td>0%</td><td>Not reported</td><td>FFT for feature extraction, distance matrix, SVM/OCSVM for classification, 10-fold cross-validation, tested time and scalability.</td></tr><tr><td>FDF [36]</td><td>Undefended (Closed-World), WTF-PAD (Closed-World), Onion Service, Undefended (Open-World), WTF-PAD (Open-World)</td><td>87.93%</td><td>Not specified</td><td>AUC initial stage: 98.8%; AUC after 56 days: 72%</td><td>DWT-based Deep Learning.</td></tr></table>

To address these variables, it is crucial to develop systematic approaches that analyze the impact of these factors on WF performance. Additionally, there is a pressing need for robust pre-processing techniques tailored to diverse real-world conditions to enhance the applicability and reliability of WF methods.

## 2) LIMITATIONS AND GAPS

## a: LIMITATIONS

WF techniques on the Tor network come across notable limitations and contraventions in real-time situations. These exceptions entail the standardized datasets, struggling to capture accurate real-world traffic, and facing the complexity of handling multifaceted users’ behaviors and system configurations. Tackling these deficiencies is critical for nuancing the reliability of WF techniques.

TABLE 3. (Continued.) Benchmark of WF.

<table><tr><td>Algorithms</td><td>Dataset</td><td>Accuracy</td><td>False Positives</td><td>AUC (Concept Drift)</td><td>Methodologies</td></tr><tr><td>CorrClassifier [37]</td><td>Rimmer et al.&#x27;s Dataset</td><td>95%</td><td>4.5%</td><td>Not reported</td><td>Uses initial direction-based preprocessing with correlation analysis.</td></tr><tr><td>CPWF [38]</td><td>Android Dataset, Windows Dataset</td><td>94.9% in single platform, 87.1% in cross-platform</td><td>Low (Not specified exact value)</td><td>Single platform AUC initial stage: 94.9%; AUC after 30 days: 93.5%; Cross platform AUC initial stage: 87.1%; AUC after 30 days: 85.2%</td><td>Single platform evaluated using cross-validation and multi-similarity loss-based feature extraction; Cross-platform tested with cross-validation using deep metric learning to extract cross-device features.</td></tr><tr><td>TinyWFP [40]</td><td>CW100, CW95, OW95, WTF-PAD95, W-T100</td><td>99.2%</td><td>4.6%</td><td>AUC initial stage: 96%; AUC after 30 days: 79%</td><td>Evaluated on CW100, CW95, OW95, WTF-PAD95, W-T100 datasets using AUC (concept drift), FPR, and inference time in closed-world and open-world scenarios.</td></tr><tr><td>Wavelet Transform + SVM (Polynomial Kernel) [41]</td><td>DS1, DS2</td><td>96.7%</td><td>4.6%</td><td>AUC initial stage: 96%; AUC after 30 days: 79%; AUC after 56 days: 76%</td><td>Evaluated on DS1 and DS2 with 10-fold cross-validation.</td></tr><tr><td>Bit-FP [60]</td><td>Bitcoin Hidden Node, CIC Darknet, Websites Hidden Services</td><td>98.96%</td><td>1.4%</td><td>AUC initial stage: 96%; AUC after 30 days: 79%; AUC after 56 days: 76%</td><td>Evaluated using 10-fold cross-validation on a combination of Bitcoin hidden node and Tor traffic datasets. Uses TLS packet size and direction as key features.</td></tr><tr><td>Decision Tree, Random Forest, KNN, GBDT [63]</td><td>Access Network, Core Gateway</td><td>91.88%</td><td>5.5%</td><td>AUC initial stage: 91.25%; AUC after 30 days: 87%; AUC after 60 days: 85%</td><td>Data collection, preprocessing, and decision tree classification. Ensemble method, parameter tuning, and cross-validation.</td></tr><tr><td>SVM, Random forest (RF), XGBoost [62]</td><td>Circuit Dataset</td><td>99.99%</td><td>0.01%</td><td>AUC initial stage: 98%; AUC after 30 days: 94%; AUC after 60 days: 91%</td><td>-Feature extraction and 10-fold cross-validation. -Ensemble method with parameter tuning. -Gradient boosting and hyperparameter optimization.</td></tr></table>

## b: GAPS

Research gaps originated from unclear conclusions, making it understandable how WF performance is affected by specific limitations. For example, scarcity of empirical data exists on the impact of browser settings, browser extensions, and patterns of user engagement on WF accuracy. The necessity of deep analysis and innovative methodologies can overcome these gaps to further enhance WF approaches.

Overcoming the identified limitations and gaps, some essential recommendations are highlighted in Table 5.

TABLE 3. (Continued.) Benchmark of WF.

<table><tr><td>Algorithms</td><td>Dataset</td><td>Accuracy</td><td>False Positives</td><td>AUC (Concept Drift)</td><td>Methodologies</td></tr><tr><td>Random Forest [73]</td><td>DS-19mt</td><td>99.96%</td><td>0.01%</td><td>AUC initial stage: 99% AUC after 30 days: 99%; AUC after 56 days: 70.49%</td><td>-Implemented feature extraction, 10-fold cross-validation, ensemble methods with parameter tuning, and gradient boosting with hyperparameter optimization.</td></tr><tr><td>Extremely Randomized Tree [66]</td><td>Same-Source, Multi-source, Background</td><td>93.63%</td><td>0.4%</td><td>AUC initial stage: 98.30%</td><td>Uses extremely randomized trees with response time features for accurate classification in dynamic environments.</td></tr><tr><td>Triplet Fingerprinting (TF) [42]</td><td>Wang100, AWF100, DF95</td><td>95%</td><td>3%</td><td>Not reported</td><td>Uses triplet networks with N-shot learning for improved WF under varying conditions.</td></tr><tr><td>(BAPM) [43]</td><td>Real-world multi-tab</td><td>93.2%</td><td>2.5%</td><td>Not reported</td><td>Uses CNN for tab-aware representation and multi-head .</td></tr><tr><td>AdaWFPA [44]</td><td>KNNdata, Walkie-Talkie</td><td>99.60%</td><td>3%</td><td>Not reported</td><td>Uses Adaptive Hoeffding Tree and Option Tree with streaming data handling</td></tr><tr><td>TPR [47]</td><td>Simulated hidden service request rates (26k, 43k, 65k/day) on the live tor network</td><td>96.45%</td><td>0% for 26k/day, 8.6% for 43k/day, 72% for 65k/day</td><td>Not reported</td><td>Combining circuiting fingerprinting (position analysis), traffic direction analysis and timing-based traffic recognition</td></tr><tr><td>PCDB [46]</td><td>Custom Tor traffic captures</td><td>100%</td><td>0%</td><td>Not reported</td><td>Analyzes packets count within 3 seconds of SYN packets to distinguish Tor clients/Hidden services</td></tr><tr><td>TFAN [67]</td><td>AWF900 (closed-world), AWFUM400k (open-world), DS-19 (defended: WTF-PAD/FRONT)</td><td>95.6%</td><td>&lt;5%</td><td>Binary-Class with 1 shot initial stage: 93.2%; After 30 days: 90.4%; Multi-class initial stage:90.6%; performance drops after 30 days: 87.5%</td><td>Uses meta-learning along with task-adaptive feature alignment (ridge regression+ channel modulation) for few shots website fingerprinting</td></tr></table>

The creation of new, holistic datasets that capture the realistic user’s online actions and a variety of systems is the most crucial step. Most of the existing datasets are incapable of adequately representing the variability present in real-world traffic, compromising the effectiveness of these datasets for advancing the WF approaches.

With the generation of heterogeneous and high-quality datasets, researchers can further enhance the WF accuracy, robustness, and generalizability. These initiatives will not only strengthen the Tor network’s anonymity but will also enhance the performance of the WF attack.

TABLE 3. (Continued.) Benchmark of WF.

<table><tr><td>Algorithms</td><td>Dataset</td><td>Accuracy</td><td>False Positives</td><td>AUC (Concept Drift)</td><td>Methodologies</td></tr><tr><td>TIOD [68]</td><td>Two-Tab Dataset, Three-Tab Dataset, GLUE Defense Dataset, Open-World Dataset</td><td>85%</td><td>Not Specified</td><td>Not reported</td><td>Converts Tor traces to 2D images; uses object detection (RPN-M) to classify overlapping tab features</td></tr><tr><td>Packet removal + feature fusion [65]</td><td>General Websites, Onion Services</td><td>98.3%</td><td>2%</td><td>Not reported</td><td>Packet removal + feature fusion (CUMUL + 125 features → 81/90/140 sets)</td></tr><tr><td>CTWF [69]</td><td>AWF-100, AWF-200, AWF-500, AWF-900, DF (WTF-PAD defense), Open-world (AWF-ow), Time-drift (AWF-d)</td><td>99.42%</td><td>Not reported</td><td>Not reported</td><td>Combining of Compact convolution Transformer with burst-sequence feature extraction and sequence pooling to classify the Tor traffic</td></tr><tr><td>FD-WF [71]</td><td>Single-tab, multi-tab (2-tab)</td><td>98.61%</td><td>Not reported</td><td>Not reported</td><td>Minimum Padding Optimization for improving the performance of fixed-dimension image generation</td></tr><tr><td>LASERBEAK [72]</td><td>Big Enough, Gong-Surakav, Single-Site</td><td>96%</td><td>Not reported</td><td>Not reported</td><td>Big Enough, Gong-Surakav, Single-Site</td></tr><tr><td>Holmes [74]</td><td>Alexa-top websites, dark web websites, Front defense, Walkie-Talkie, Traffic Sliver</td><td>98.63%</td><td>Not reported</td><td>Not reported</td><td>Employs supervised contrastive learning and utilization of temporal distribution for embedding traffic into low-dimensional feature space and to achieve website-adaptive data augmentation</td></tr></table>

## 3) ETHICAL IMPLICATIONS, MISUSE, AND RESEARCH BOUNDARIES

## a: WFAS A DUAL-USE

It can strengthen privacy defenses, but also enable surveillance, profiling, and censorship by inferring visited sites from encrypted traffic.

## b: MISUSE RISKS

Targeted monitoring of sensitive browsing, discrimination/profiling, traffic filtering/throttling, and operational deanonymization of at-risk users.

## c: RESEARCH BOUNDARIES

Avoid real-user targeting; use consenting participants/ testbeds; minimize and secure data (de-identify, restrict access, short retention); obtain IRB/ethics review where applicable; practice responsible disclosure; and publish with care (share defensive insights/benchmarks, avoid releasing turnkey attack tooling or highly targetable models).

## 4) SUMMARIZATION

Regardless of the significant strides made by researchers in the Website fingerprinting research, the limitations corresponds to making it clear and comprehending the impact of browser settings, plugins and user online activities on WF assaults. To overcome these gaps, researchers must come up with the idea of creating realistic datasets and standardized benchmarks, which will provide a framework for subsequent research and enhance developments in the domain area of WF on the Tor network

TABLE 4. System performance assessment metrics.

<table><tr><td>Year</td><td>Algorithms</td><td>Computational Overhead</td><td>Scalability</td><td>Latency</td><td>Adversarial Robustness</td><td>Real-time Feasibility</td></tr><tr><td>2024</td><td>TFAN [67]</td><td>Low</td><td>High</td><td>Low (Efficient feature alignment and ridge regression)</td><td>Resilient against WTF-PAD and time shifts</td><td>Feasible (working efficiently in dynamic network environment)</td></tr><tr><td>2024</td><td>TIOD [68]</td><td>High</td><td>High for &lt;8 tabs, low for &gt;8 tabs</td><td>-</td><td>Robust to natural trace overlap but vulnerable to active defenses</td><td>Not feasible for real time; feasible for small tab count &lt;5 tabs</td></tr><tr><td>2024</td><td>RF, XGBoost, DT, ET [65]</td><td>Moderate</td><td>High</td><td>-</td><td>-</td><td>Feasible (3× faster training than CUMUL)</td></tr><tr><td>2024</td><td>Compact Convolutional Transformer [69]</td><td>Low</td><td>High</td><td>-</td><td>Resilient to time-drift and WAT-PAD defenses</td><td>Feasible for controlled environment</td></tr><tr><td>2024</td><td>FD-WF (Enhanced ResNet-18 with Sigmoid) [71]</td><td>Moderate</td><td>High</td><td>Low (converge in 50 epochs)</td><td>-</td><td>Feasible (need implementation of NVIDIA 2080Ti)</td></tr><tr><td>2024</td><td>LASERBEAK (transformer-based CNN + Attention + residual) [72]</td><td>Moderate</td><td>High</td><td>-</td><td>Robustness against state-of-the-art defenses like FRONT, Interspace, Surakav</td><td>Feasible in real time with GPU acceleration</td></tr><tr><td>2024</td><td>SCL + CCN Encoder + Shap-based feature attribution [74]</td><td>Moderate</td><td>High</td><td>Low (45.25s avg. for dark web, 21.71%-page load ratio)</td><td>Resilient against WTF-PAD, Walkie-talkie, Traffic-Silver attack</td><td>Feasible in both offline and online</td></tr><tr><td>2023</td><td>Fed-Fingerprinting (FL + Feature selection + Tor Node Selection) [30]</td><td>18% lower training time vs raw data (feature engineering)</td><td>High</td><td>-</td><td>-</td><td>Feasible (achieves 85% accuracy with fast convergence)</td></tr></table>

TABLE 4. (Continued.) System performance assessment metrics

<table><tr><td>Year</td><td>Algorithms</td><td>Computational Overhead</td><td>Scalability</td><td>Latency</td><td>Adversarial Robustness</td><td>Real-time Feasibility</td></tr><tr><td>2023</td><td>ARES [31][20]</td><td>Very High</td><td>High</td><td>~0.26-0.42s per website classifier</td><td>Achieves 84% AUC vs WTF-PAD, 76% vs front defenses</td><td>Parallelizable architecture, Processing multi-classifier simultaneously, Resource intensive</td></tr><tr><td>2023</td><td>CWFA (1D-CNN with direction + Timing fusion) [33]</td><td>Moderate</td><td>High</td><td>-</td><td>Show resilient against WTF-PAD and Front defenses</td><td>Feasible (Reasonable training time, fine-tune mechanism support updates)</td></tr><tr><td>2021</td><td>DNNF [34]</td><td>High</td><td>Moderate</td><td>-</td><td>Can handle concept drift, but not tested against active defenses</td><td>Not feasible for real-time, fit for offline analysis</td></tr><tr><td>2022</td><td>snWF (depth-wise separable convolution + attention) [32]</td><td>Low</td><td>High</td><td>-</td><td>More robust against concept drift than DF, CNN-R, VAR-CNN</td><td>Feasible (efficient training and inference)</td></tr><tr><td>2019</td><td>FFT [35]</td><td>Low</td><td>High</td><td>&lt;2 seconds per detection</td><td>Resilient against lightweight defenses</td><td>Feasible online, updates every minute</td></tr><tr><td>2022</td><td>FDF [36]</td><td>Moderate</td><td>High</td><td>-</td><td>Robust against WTF-PAD defenses</td><td>Feasible for training (batch processing with deep learning, but large data sets are required)</td></tr><tr><td>2023</td><td>Corr-classifier [37]</td><td>Low</td><td>High</td><td>Low (first 100-1000 packets used)</td><td>Resilient to network noises</td><td>Feasible (complexity reduces through low-dimension correlation)</td></tr><tr><td>2020</td><td>CPWF (Multi-Similarity Loss + CNN) [38]</td><td>High</td><td>High</td><td>-</td><td>Resilient to cross-platform variations, not tested on countermeasures</td><td>Feasible (for specific targeted attacks, Not feasible for large scale-dragnet)</td></tr></table>

TABLE 4. (Continued.) System performance assessment metrics

<table><tr><td>Year</td><td>Algorithms</td><td>Computational Overhead</td><td>Scalability</td><td>Latency</td><td>Adversarial Robustness</td><td>Real-time Feasibility</td></tr><tr><td>2023</td><td>Tiny WFP (Wavelet + lightweight NN) [40]</td><td>Low</td><td>High</td><td>Low(545ms for 1k instances;15× faster than DF,55× faster than VAR-CNN)</td><td>More resilient against WTF-PAD defense, Limited robust against W-T defense</td><td>Feasible (deployable on weaker attackers like routers/trojans)</td></tr><tr><td>2019</td><td>Wavelet transform (DB4) + SVM [41]</td><td>Moderate</td><td>High</td><td>-</td><td>Resilient to padding, multi-tab browsing</td><td>Conditionally feasible</td></tr><tr><td>2021</td><td>Bit-FP (Random decision forest) [60]</td><td>Low</td><td>High</td><td>-</td><td>Robust against Cell padding, Traffic morphing, Randomized packet timing</td><td>Highly feasible (works with sequences as short as 20 packets)</td></tr><tr><td>2021</td><td>Decision tree, Random Tree, KNN, GBDT [63]</td><td>Access: Moderate (Decision tree/KNN dominant) Core: High (RF/GBDT)</td><td>Access: High, Core: Moderate</td><td>-</td><td>-</td><td>Feasible in access network, limited in core network</td></tr><tr><td>2023</td><td>SVM, Random Forest, XGBoost [62]</td><td>Moderate</td><td>High</td><td>-</td><td>Robust against Tor padding based defenses and adaptive obfuscation technique</td><td>Feasible (practically in real world deployment)</td></tr><tr><td>2022</td><td>WFD [73]</td><td>High</td><td>High</td><td>Low (attack achieves 1208.30 Mbps)</td><td>Robust against GLUE defense</td><td>Feasible in real-world, practical online deployment</td></tr><tr><td>2020</td><td>WRFP (extremely randomized tree) [66]</td><td>Low</td><td>High</td><td>Low (tolerates 10% time fluctuations)</td><td>Resilient against lightweight defenses</td><td>Feasible (93% TPR in real-world tests)</td></tr></table>

TABLE 4. (Continued.) System performance assessment metrics

<table><tr><td>Year</td><td>Algorithms</td><td>Computational Overhead</td><td>Scalability</td><td>Latency</td><td>Adversarial Robustness</td><td>Real-time Feasibility</td></tr><tr><td>2019</td><td>Triplet fingerprinting [42]</td><td>Low</td><td>High</td><td>-</td><td>Resilient to data mismatch (85% with 3-year-old training data)</td><td>Feasible (practical for real-world deployment)</td></tr><tr><td>2021</td><td>BAPM [43]</td><td>-</td><td>High</td><td>-</td><td>Robust to overlapping areas and multi-tab scenarios</td><td>Feasible for real-time deployment</td></tr><tr><td>2019</td><td>AdaWFPA (Adaptive Hoeffding Tree + Option Tree) [44]</td><td>Low</td><td>High</td><td>Low (real time, incremental updates)</td><td>Robust to dynamic updates and concept drift</td><td>Feasible (processes the examples as fast as possible, avoids data loss)</td></tr><tr><td>2021</td><td>Traffic pattern recognition [47]</td><td>Low</td><td>Moderate</td><td>High</td><td>Low (defeated by Tor padding cells)</td><td>Not feasible (processes the examples as fast as possible, avoids data loss)</td></tr><tr><td>2020</td><td>Packet-count-based-detection [46]</td><td>Low</td><td>Limited</td><td>Low</td><td>Low (vulnerable to client configuration)</td><td>Feasible (for target monitoring)</td></tr></table>

and hurdles pointed out above emphasize the need for further innovations. Specifically pressing open questions

TABLE 5. Limitations, gaps, and recommendations in website fingerprinting on tor.

<table><tr><td>Limitations</td><td>Gaps</td><td>Recommendations</td></tr><tr><td>Many studies on website fingerprinting focus on single and multiple client settings within similar systems and network environments.</td><td>What is the impact of website fingerprinting on multiple Tor users that are connected to distinguish systems, but in a similar environment?</td><td>utilizing the dataset gathered using multiple system configurations within the analogous system to effectively address the limitations and enrich the generalizability of findings.</td></tr><tr><td>Measuring Tor users&#x27; browsing habits and estimating the significance of its assumption is very challenging.</td><td>There is a lack of analysis on how observing a dedicated group&#x27;s daily activities affects website fingerprinting effectiveness.</td><td>Let&#x27;s take into consideration the possibility of observing an important volunteer group&#x27;s online activities that regularly make use of the Tor browser in their daily routines.</td></tr><tr><td>Lack of detailed analysis on the recognition of various webpages per site is often observed.</td><td>The impact of consecutive browsing of internal webpages on the effectiveness of website fingerprinting is not well-explored.</td><td>Perform experiments using a dataset gathered through a consecutive browsing session to evaluate its impact on fingerprinting efficiency.</td></tr></table>

## VII. CONCLUSION

The main goal of fingerprinting attacks on the Tor network is to compromise its anonymity and reveal the online browsing activities of its users. This survey paper has presented a thorough examination of Tor and its hidden services, offering a comprehensive review of fingerprinting techniques aimed at de-anonymizing Tor users. To the best of our knowledge, there is a lack of research that systematically examines and evaluates the fingerprinting techniques applied to the Tor network.

In this paper, we have reviewed research conducted over the past five years (2019–2024), covering all fingerprinting techniques deployed against the Tor network. Additionally, we introduced a taxonomy that organizes and explains the various fingerprinting methods used in Tor-related research.

While these techniques show promise, we identified key limitations and gaps that hinder the practical implementation of fingerprinting attacks for effectively detecting users’ online activities. To address these challenges, we have suggested several recommendations, providing potential directions for future research. These recommendations aim to enhance the reliability and applicability of fingerprinting techniques, guiding further developments in Tor privacy and security research.

## VIII. DECLARATION OF GENERATIVE AI AND

## AI-ASSISTED TECHNOLOGIES IN THE WRITING PROCESS

During the preparation of this work, the author(s) utilizes AI-tool ‘‘Sider’’ to polish and improve the language of the manuscript and remove any grammatical errors. As nonnative English speakers, we do not have a good grip on language skills, and there is a greater possibility that we might make mistakes during writing. These tools were brought into use to enhance the readability and clarity of the text without changing the foundational ideas and scientific data. We made sure that the originality and accuracy of the work aren’t damaged, including all ideas, analyses, and results of the paper.

## IX. DECLARATION OF COMPETING INTEREST

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## REFERENCES

[1] R. Dingledine, N. Mathewson, and P. Syverson, ‘‘Tor: The secondgeneration onion router,’’ in Proc. USENIX Secur. Symp., Aug. 2004, pp. 303–320.

[2] Tor Metrics Portal: Data. Accessed: Dec. 2024. [Online]. Available: https: //metrics.torproject.org/torperf.html

[3] A. Montieri, D. Ciuonzo, G. Aceto, and A. Pescapé, ‘‘Anonymity services tor, I2P, JonDonym: Classifying in the dark,’’ in Proc. 29th Int. Teletraffic Congr. (ITC), vol. 1, Sep. 2017, pp. 81–89.

[4] J. Aldridge and R. Askew, ‘‘Delivery dilemmas: How drug cryptomarket users identify and seek to reduce their risk of detection by law enforcement,’’ Int. J. Drug Policy, vol. 41, pp. 101–109, Mar. 2017.

[5] J. Broséus, D. Rhumorbarbe, M. Morelato, L. Staehli, and Q. Rossy, ‘‘A geographical analysis of trafficking on a popular darknet market,’’ Forensic Sci. Int., vol. 277, pp. 88–102, Aug. 2017.

[6] P. Winter, R. Köwer, M. Mulazzani, M. Huber, S. Schrittwieser, S. Lindskog, and E. Weippl, ‘‘Spoiled onions: Exposing malicious tor exit relays,’’ in Proc. Privacy Enhancing Technol. Symp., 2014, pp. 304–331.

[7] Y. Okada, S. Ata, N. Nakamura, Y. Nakahira, and I. Oka, ‘‘Application identification from encrypted traffic based on characteristic changes by encryption,’’ in Proc. IEEE Int. Workshop Tech. Committee Commun. Quality Rel. (CQR), May 2011, pp. 1–6.

[8] D. McCoy, K. Bauer, D. Grunwald, T. Kohno, and D. Sicker, ‘‘Shining light in dark places: Understanding the tor network,’’ in Proc. Privacy Enhancing Technol. Symp., 2008, pp. 63–76.

[9] A. Almubayed, A. Hadi, and J. Atoum, ‘‘A model for detecting tor encrypted traffic using supervised machine learning,’’ Int. J. Comput. Netw. Inf. Secur., vol. 7, no. 7, pp. 10–23, Jun. 2015, doi: 10.5815/ijcnis.2015.07.02.

[10] A. Panchenko, A. Mitseva, M. Henze, F. Lanze, K. Wehrle, and T. Engel, ‘‘Analysis of fingerprinting techniques for tor hidden services,’’ in Proc. Workshop Privacy Electron. Soc., Oct. 2017, pp. 165–175, doi: 10.1145/3139550.3139564.

[11] M. Yang, X. Gu, Z. Ling, C. Yin, and J. Luo, ‘‘An active de-anonymizing attack against tor web traffic,’’ Tsinghua Sci. Technol., vol. 22, no. 6, pp. 702–713, Dec. 2017.

[12] M. A. I. Mohd Aminuddin, Z. F. Zaaba, A. Samsudin, F. Zaki, and N. B. Anuar, ‘‘The rise of website fingerprinting on tor: Analysis on techniques and assumptions,’’ J. Netw. Comput. Appl., vol. 212, Mar. 2023, Art. no. 103582.

[13] A. Panchenko, L. Niessen, A. Zinnen, and T. Engel, ‘‘Website fingerprinting in onion routing based anonymization networks,’’ in Proc. 10th Annu. ACM Workshop Privacy Electron. Soc., Oct. 2011, pp. 103–114.

[14] D. Herrmann, R. Wendolsky, and H. Federrath, ‘‘Website fingerprinting: Attacking popular privacy enhancing technologies with the multinomia naïve-Bayes classifier,’’ in Proc. ACM workshop Cloud Comput. Secur., Nov. 2009, pp. 31–42.

[15] P. Laperdrix, N. Bielova, B. Baudry, and G. Avoine, ‘‘Browser fingerprint ing: A survey,’’ IEEE Trans. Web, vol. 14, no. 2, pp. 1–33, Feb. 2020.

[16] H. Kumar and P. Dixit, ‘‘Achieving anonymity with the help of TOR,’ 2015.

[17] M. A. I. M. Aminuddin, Z. Fitri, M. Kaur, and D. Singh, ‘‘A survey on tor encrypted traffic monitoring,’’ Int. J. Adv. Comput. Sci. Appl., vol. 9, no. 8, pp. 113–120, 2018.

[18] M. G. Reed, P. F. Syverson, and D. M. Goldschlag, ‘‘Anonymous connections and onion routing,’’ IEEE J. Sel. Areas Commun., vol. 16, no. 4, pp. 482–494, May 1998.

[19] P. Syverson, ‘‘A peel of onion,’’ in Proc. 27th Annu. Comput. Secur. Appl. Conf., Dec. 2011, pp. 123–137.

[20] G. Owen and N. Savage, The Tor Dark Net. London, U.K.: Centre fo International Governance Innovation (CIGI) and Chatham House, 2015.

[21] J. Bian, C. Cao, L. Wang, J. Ye, Y. Zhao, and C. Tang, ‘‘Tor hidden services discovery and analysis: A literature survey,’’ J. Phys., Conf. Ser., vol. 1757, no. 1. Jan. 2021, Art, no. 012162

[22] I. Sanchez-Rola, D. Balzarotti, and I. Santos, ‘‘The onions have eyes: A comprehensive structure and privacy analysis of tor hidden services,’’ in Proc. 26th Int. Conf. World Wide Web, Apr. 2017, pp. 1251–1260.

[23] M. Bernaschi, A. Celestini, S. Guarino, F. Lombardi, and E. Mastrostefano, ‘‘Spiders like onions: On the network of tor hidden services,’’ in Proc World Wide Web Conf., May 2019, pp. 105–115.

[24] X. Cai, R. Nithyanand, T. Wang, R. Johnson, and I. Goldberg, ‘‘A systematic approach to developing and evaluating website fingerprinting defenses,’’ in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2014, pp. 227–238.

[25] X. Cai, X. C. Zhang, B. Joshi, and R. Johnson, ‘‘Touching from a distance: Website fingerprinting attacks and defenses,’’ in Proc. ACM Conf. Comput. Commun. Secur., Oct. 2012, pp. 605–616.

[26] T. Wang, X. Cai, R. Nithyanand, R. Johnson, and I. Goldberg, ‘‘Effective attacks and provable defenses for website fingerprinting,’’ in Proc. 23rd USENIX Secur. Symp. (USENIX Secur.), 2014, pp. 143–157.

[27] C. Luo, W. Tang, Q. Wang, and D. Zheng, ‘‘Few-shot website finger printing with distribution calibration,’’ IEEE Trans. Dependable Secure Comput., vol. 22, no. 1, pp. 632–648, Jan. 2025.

[28] T. Wang and I. Goldberg, ‘‘Improved website fingerprinting on tor,’ in Proc. 12th ACM Workshop Privacy Electron. Soc., Nov. 2013, pp. 201–212.

[29] T. Wang and I. Goldberg, ‘‘On realistically attacking tor with website fingerprinting,’’ Proc. Privacy Enhancing Technol., vol. 2016, no. 4, pp. 21–36, Oct. 2016.

[30] J. Bang, J. Jeong, and J. Lee, ‘‘FedFingerprinting: A federated learning approach to website fingerprinting attacks in tor networks,’’ IEEE Access, vol. 11, pp. 78431–78444, 2023.

[31] X. Deng, Q. Yin, Z. Liu, X. Zhao, Q. Li, M. Xu, K. Xu, and J. Wu, ‘‘Robust multi-tab website fingerprinting attacks in the wild,’’ in Proc. IEEE Symp. Secur. Privacy (SP), May 2023, pp. 1005–1022.

[32] Y. Wang, H. Xu, Z. Guo, Z. Qin, and K. Ren, ‘‘SnWF: Website fingerprinting attack by ensembling the snapshot of deep learning,’’ IEEE Trans. Inf. Forensics Security, vol. 17, pp. 1214–1226, 2022.

[33] T. Pan, Z. Tang, and D. Xu, ‘‘A practical website fingerprinting attack via CNN-based transfer learning,’’ Mathematics, vol. 11, no. 19, p. 4078, Sep. 2023.

[34] M. Guo, J. Fei, and Y. Meng, ‘‘Deep nearest neighbor website finger printing attack technology,’’ Secur. Commun. Netw., vol. 2021, pp. 1–14, Jul. 2021.

[35] H. Jahani and S. Jalili, ‘‘Online tor privacy breach through website fingerprinting attack,’’ J. Netw. Syst. Manage., vol. 27, no. 2, pp. 289–326, Apr. 2019.

[36] Y. Sun, X. Luo, H. Wang, and Z. Ma, ‘‘A method for identifying tor users visiting websites based on frequency domain fingerprinting of network traffic,’’ Secur. Commun. Netw., vol. 2022, pp. 1–12, Jan. 2022.

[37] R. Attarian and A. Keshavarz-Haddad, ‘‘Effective website fingerprinting attack based on the first packet direction only,’’ Comput. Netw., vol. 231, Jul. 2023, Art. no. 109811.

[38] S. Wang, L. Wang, S. Yin, H. Zhao, and H. Shentu, ‘‘CPWF: Cross platform website fingerprinting based on multi-similarity loss,’’ in Proc. Int. Conf. Netw. Netw. Appl. (NaNA), Dec. 2020, pp. 73–80.

[39] X. Wang, X. Han, W. Huang, D. Dong, and M. R. Scott, ‘‘Multi-similarity loss with general pair weighting for deep metric learning,’’ in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2019, pp. 5017–5025.

[40] C. Tian, D. Ye, and C. Chen, ‘‘Tiny WFP: Lightweight and effective website fingerprinting via wavelet multi-resolution analysis,’’ in Proc. Int. Conf. Appl. Cryptogr. Netw. Secur., 2023, pp. 237–259.

[41] Q. Lai and J. Ling, ‘‘An anonymous network website fingerprinting attack method based on wavelet transformation,’’ J. Phys., Conf. Ser., vol. 1302, no. 2, Aug. 2019, Art. no. 022074.

[42] P. Sirinam, N. Mathews, M. S. Rahman, and M. Wright, ‘‘Triplet fingerprinting: More practical and portable website fingerprinting with Nshot learning,’’ in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2019, pp. 1131–1148.

[43] Z. Guan, G. Xiong, G. Gou, Z. Li, M. Cui, and C. Liu, ‘‘BAPM: Block attention profiling model for multi-tab website fingerprinting attacks on tor,’’ in Proc. Annu. Comput. Secur. Appl. Conf., Dec. 2021, pp. 248–259.

[44] R. Attarian, L. Abdi, and S. Hashemi, ‘‘AdaWFPA: Adaptive online website fingerprinting attack for tor anonymous network: A stream-wise paradigm,’’ Comput. Commun., vol. 148, pp. 74–85, Dec. 2019.

[45] T. Lu, T. Meng, C. Li, G. Dong, H. Li, J. Zhang, and X. Zhang, ‘‘MSFA: Multiple system fingerprint attack scheme for IoT anonymous communication,’’ Secur. Commun. Netw., vol. 2019, pp. 1–15, Mar. 2019.

[46] F. Platzer, M. Schäfer, and M. Steinebach, ‘‘Critical traffic analysis on the tor network,’’ in Proc. 15th Int. Conf. Availability, Rel. Secur., Aug. 2020, pp. 1–10.

[47] N. Yoshiura and K. Koizumi, ‘‘A method of collecting the IP addresses of hidden server in tor networks,’’ in Proc. 9th Int. Conf. Softw. Comput. Appl., Feb. 2020, pp. 242–246.

[48] K. Kohls and C. Pöpper, ‘‘DigesTor: Comparing passive traffic analysis attacks on Tor,’’ in Proc. 23rd Eur. Symp. Res. Comput. Secur. (ESORICS), 2018, pp. 512–530.

[49] L. Basyoni, N. Fetais, A. Erbad, A. Mohamed, and M. Guizani, ‘‘Traffic analysis attacks on tor: A survey,’’ in Proc. IEEE Int. Conf. Informat., IoT, Enabling Technol. (ICIoT), Feb. 2020, pp. 183–188.

[50] T. D. Polyzos, ‘‘Tor circuit fingerprinting: Attacks and defenses,’’ IEEE Access, pp. 1–40, Feb. 2021.

[51] E. Petagna, G. Laurena, C. Ciccotelli, and L. Querzoni, ‘‘Peel the onion: Recognition of Android apps behind the tor network,’’ in Proc. Int. Conf. Inf. Secur. Pract. Exper., 2019, pp. 95–112.

[52] L. Wang, H. Mei, and V. S. Sheng, ‘‘Multilevel identification and classification analysis of tor on mobile and PC platforms,’’ IEEE Trans. Ind. Informat., vol. 17, no. 2, pp. 1079–1088, Feb. 2021.

[53] X. Fu, Z. Ling, J. Luo, W. Yu, W. Jia, and W. Zhao, ‘‘One cell is enough to break tor’s anonymity,’’ in Proc. Black Hat Tech. Secur. Conf., 2009, pp. 578–589.

[54] S. E. Oh, S. Li, and N. Hopper, ‘‘Fingerprinting keywords in search queries over tor,’’ Proc. Privacy Enhancing Technol., vol. 2017, no. 4, pp. 251–270, Oct. 2017.

[55] K. Bauer, D. Grunwald, and D. Sicker, ‘‘Predicting Tor path compromise by exit port,’’ in Proc. IEEE 28th Int. Perform. Comput. Commun. Conf. New York, NY, USA: Institute of Electrical and Electronics Engineers (IEEE), 2009, pp. 384–387.

[56] P. Choorod, G. Weir, and A. Fernando, ‘‘Classifying tor traffic encrypted payload using machine learning,’’ IEEE Access, vol. 12, pp. 19418–19431, 2024.

[57] A. Habibi Lashkari, G. Draper Gil, M. S. I. Mamun, and A. A. Ghorbani, ‘‘Characterization of tor traffic using time based features,’’ in Proc. 3rd Int. Conf. Inf. Syst. Secur. Privacy, 2017, pp. 253–262.

[58] Y. Xu, J. Li, Y. Hou, L. Wang, K. Song, and G. Cheng, ‘‘NuanceTracker: A website fingerprinting attack against tor hidden services through burst patterns,’’ in Proc. IEEE Symp. Comput. Commun. (ISCC), Jun. 2024, pp. 1–7.

[59] K. Kohls, K. Jansen, D. Rupprecht, T. Holz, and C. Popper, ‘‘On the challenges of geographical avoidance for tor,’’ in Proc. Netw. Distrib. Syst. Secur. Symp., 2019, pp. 1–15.

[60] K. Zou, J. Shi, Y. Gao, X. Wang, M. Wang, Z. Li, and M. Su, ‘‘Bit-FP: A traffic fingerprinting approach for Bitcoin hidden service detection,’’ in Proc. IEEE 6th Int. Conf. Data Sci. Cyberspace (DSC), Oct. 2021, pp. 99–105.

[61] G. Cherubin, R. Jansen, and C. Troncoso, ‘‘Online website fingerprinting: Evaluating website fingerprinting attacks on tor in the real world,’’ in Proc. USENIX Secur. Symp. (USENIX Secur.), 2022, pp. 753–770.

[62] B. Huang and Y. Du, ‘‘Discovering onion services through circuit fin gerprinting attacks,’’ High-Confidence Comput., vol. 3, no. 1, Mar. 2023, Art. no. 100099.

[63] H. Mei, G. Cheng, W. Gao, and J. Chen, ‘‘Website fingerprinting on access network and core gateway,’’ in Proc. 17th Int. Conf. Mobility, Sens. Netw. (MSN), Dec. 2021, pp. 671–678.

[64] Y. Chen, Y. Wang, L. Yang, Y. Luo, and M. Chen, ‘‘TForm-RF: An efficient data augmentation for website fingerprinting attack,’’ in Proc. IEEE Int. Perform., Comput., Commun. Conf. (IPCCC), Nov. 2022, pp. 169–178.

[65] D. Kim, A. Booth, O. Akinyemi, E. Choo, and D. Hwang, ‘‘Website fingerprinting attacks with advanced features on tor networks,’’ in Proc. Cyber Awareness Res. Symp. (CARS), Oct. 2024, pp. 1–6.

[66] Y. Meng and J. Fei, ‘‘Hidden service website response fingerprinting attacks based on response time feature,’’ Secur. Commun. Netw., vol. 2020, pp. 1–21, Nov. 2020.

[67] Q. Lyu, H. Xie, W. Wang, Y. Cheng, Y. Chen, and Z. Wang, ‘‘TFAN: A task adaptive feature alignment network for few-shot website fingerprinting attacks on tor,’’ Comput. Secur., vol. 144, Sep. 2024, Art. no. 103980.

[68] Y. Xu, L. Wang, J. Chen, and Q. Zhou, ‘‘Tor trace in images: A novel multi-tab website fingerprinting attack with object detection,’’ Comput. J., vol. 67, no. 8, pp. 2690–2701, Aug. 2024.

[69] G. Lyu, J. Kong, Y. Chen, and F. Wang, ‘‘CTWF: Website fingerprinting attack based on compact convolutional transformer,’’ in Proc. IEEE 23rd Int. Conf. Trust, Secur. Privacy Comput. Commun. (TrustCom), Dec. 2024, pp. 57–67.

[70] X. Xiao, X. Zhou, Z. Yang, L. Yu, B. Zhang, Q. Liu, and X. Luo, ‘‘A comprehensive analysis of website fingerprinting defenses on tor,’ Comput. Secur., vol. 136, Jan. 2024, Art. no. 103577.

[71] R. Zhang, S. Yin, and J. Chen, ‘‘FD-WF: A multi-tab website fingerprinting attack based on fixed dimensions for tor network,’’ in Proc. IEEE 23rd Int. Conf. Trust, Secur. Privacy Comput. Commun. (TrustCom), Dec. 2024, pp. 2051–2059.

[72] N. Mathews, J. K. Holland, N. Hopper, and M. Wright, ‘‘Laserbeak: Evolving website fingerprinting attacks with attention and multi-channel feature representation,’’ IEEE Trans. Inf. Forensics Security, vol. 19, pp. 9285–9300, 2024.

[73] M. Chen, Y. Chen, Y. Wang, P. Xie, S. Fu, and X. Zhu, ‘‘End-to-end multi-tab website fingerprinting attack: A detection perspective,’’ 2022, arXiv:2203.06376.

[74] X. Deng, Q. Li, and K. Xu, ‘‘Robust and reliable early-stage web site fingerprinting attacks via spatial–temporal distribution analysis,’ in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Dec. 2024, pp. 1997–2011.

[75] E. Cambiaso, I. Vaccari, L. Patti, and M. Aiello, ‘‘Darknet security: A categorization of attacks to the tor network,’’ in Proc. ITASEC, 2019, pp. 1–12.

[76] S. Nepal, S. Dahal, and S. Shin, ‘‘Deanonymizing schemes of hidden services in tor network: A survey,’’ in Proc. Int. Conf. Inf. Netw. (ICOIN), Jan. 2015, pp. 468–473.

[77] Z. Guo, B. Lu, W. Wu, M. Guo, Z. Liu, and X. Lin, ‘‘A semi-supervised learning framework for encrypted traffic classification based on supervised contrastive learning and masked sequence prediction tasks,’’ in Proc. 8th Int. Conf. Adv. Algorithms Control Eng. (ICAACE), Mar. 2025, pp. 1882–1893.

[78] W. Meng, C. Ma, M. Ding, C. Ge, Y. Qian, and T. Xiang, ‘‘Beyond single tabs: A transformative few-shot approach to multi-tab website fingerprint ing attacks,’’ in Proc. ACM Web Conf., Apr. 2025, pp. 1068–1077.

[79] Z. Yi, T. Li, M. Zhang, X. Yuan, S. Du, and X. Luo, ‘‘An efficient website fingerprinting for new websites emerging based on incremental learning,’ IEEE Trans. Netw. Service Manage., vol. 23, pp. 365–381, 2026.

[80] D. Kim, A. Booth, and D. Hwang, ‘‘An empirical study: Feasibility of website fingerprinting attacks in real-time environments on V3 onion services,’’ in Proc. IEEE 15th Annu. Comput. Commun. Workshop Conf. (CCWC). Jan. 2025 pp. 00324–00330

[81] Y. Li, Y. Xu, X. Fan, Y. Hou, Y. Yuan, Q. Xiang, and G. Cheng, ‘‘CoDA: Cross-domain few-shot website fingerprinting via contrastive prototype alignment,’’ in Proc. IEEE 24th Int. Conf. Trust, Secur. Privacy Comput Commun. (TrustCom). Nov, 2025, pp. 1752-1758.

[82] X. Deng, R. Zhao, Y. Wang, M. Zhan, Z. Xue, and Y. Wang, ‘‘Countmamba: A generalized website fingerprinting attack via coarse grained representation and fine-grained prediction,’’ in Proc. IEEE Symp Secur. Privacy (SP), May 2025, pp. 1419–1437.

![](images/2890c06b64d10d0b8e783e5ab90d14ac9a115efeb79f596dffdff2c74a546fcf.jpg)  
FAISAL MURAD received the B.S. degree in software engineering from COMSATS University Abbottabad, in 2018, and the master’s degree in computer technology from Anhui Normal University. He is currently pursuing the Ph.D. degree with Anhui University, China. His research interests include communication anonymity and privacy.

![](images/2ea81a2eef67dea9213e092ca1d20fffbe03f9fd423d16f045148eaf709a2a01.jpg)

DEPENG CHEN received the Ph.D. degree in computer science from the Universitat Autònoma de Barcelona, in 2020. He is currently a Lecturer with the School of Computer Science and Technology, Anhui University. His research interests include trustworthy artificial intelligence systems, communication anonymity, and privacy.

![](images/0775d4de4f067b40e4b04aea980bd03abdee4a253f1aab6190b73f2de76506b4.jpg)  
ROLANDO TRUJILLO-RASUA is currently a Ramon y Cajal Researcher with Rovira i Virgili University (URV). Prior to joining URV, he held a senior lecturer position with Deakin University, Australia, and a post-doctoral position at the University of Luxembourg. His work appears in the most important publication venues in computer security, such as ACM CCS, S&P, ESORICS, and CSF. His research interests include formal methods, computer security, and privacy protection.

![](images/1f03d43e4b438e17da1d9aa8e255c691e2134908c73707f3b54d72fde85250dd.jpg)

MUHAMMAD ALAMGEER KHAN received the B.S. degree in computer science from the University of Science and Technology Bannu, in 2014, and the master’s degree in control science and engineering from the University of Science and Technology of China, in 2020. He is currently a Control Engineer with Wuhan Virtue World Robot Technology Company Ltd. His research interests include wearable robotics, solar panel cleaning robots with a focus on human enhancement, soft

robotics manipulation, and underwater swimming exoskeleton robots.