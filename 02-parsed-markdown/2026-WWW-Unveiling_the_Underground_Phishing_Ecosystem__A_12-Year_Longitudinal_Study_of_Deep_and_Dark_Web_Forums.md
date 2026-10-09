# Unveiling the Underground Phishing Ecosystem: A 12-Year Longitudinal Study of Deep and Dark Web Forums

Dohee Kim Sungkyunkwan University Suwon, Republic of Korea dohui7557@g.skku.edu

Hui Zhao Sungkyunkwan University Suwon, Republic of Korea zhaohui0728@g.skku.edu

Doowon Kim<sup>∗</sup> University of Tennessee Knoxville, TN, USA doowon@utk.edu

Sungjae Hwang<sup>∗</sup> Sungkyunkwan University Suwon, Republic of Korea sungjaeh@skku.edu

## Abstract

Phishing is a threat in which attackers masquerade as legitimate entities to steal sensitive data. While understanding the phishing ecosystem is critical for developing efective countermeasures, prior research has largely studied phishing through post-attack data, with limited examination of the attacker’s perspective and how phishing campaigns are built. Critically, the Deep and Dark Web (D2Web) serves as the primary marketplace and knowledge-sharing platform where attackers acquire phishing tools (e.g., phishing kits), exchange techniques, and trade compromised credentials. Analyz ing D2Web forums therefore provides unique visibility into the supply chain of phishing attacks pre-deployment, enabling proac tive understanding of emerging threats and attack methodologies.

This study addresses this gap through a comprehensive analysis of 394,034 posts (343,334 unique) collected from 13 D2Web forums spanning 2013 to 2025, from which 70,055 phishing-related posts are identified. We employ a LLM-based approach to eficiently ex tract key information, including phishing attack components (e.g., credentials, phishing pages, SMTP servers), targeted services (e.g., PayPal, Netflix), and component authors. This extracted data is mapped to a seven-stage attack scenario framework derived from empirical case studies. Our analysis reveals longitudinal trends in component availability, target service distribution, post type evolution, and the most active contributors annually, while characterizing pricing dynamics across diferent attack components. The results provide the first attacker-centric, macro-level longitudi nal analysis of the phishing ecosystem, ofering insights into how phishing infrastructure and markets have evolved over more than a decade. These findings contribute to a deeper understanding of the phishing supply chain and inform more efective detection and prevention strategies.

## CCS Concepts

• Mathematics of computing → Time series analysis; • Infor mation systems → Deep web; • Social and professional topics → Phishing;

## Keywords

Phishing, Dark Web, Deep Web, D2Web, Cyber Crime

<sup>∗</sup>Corresponding authors: Doowon Kim and Sungjae Hwang.

![](images/c15ca153dcd0e0187dcc6ea897ab406147713b49296d95e23bf973d9a1a34a51.jpg)

Dohee Kim, Hui Zhao, Doowon Kim, and Sungjae Hwang. 2026. Unveiling the Underground Phishing Ecosystem: A 12-Year Longitudinal Study of Deep and Dark Web Forums. In Proceedings of the ACM Web Conference 2026 (WWW’26), April 13–17, 2026, Dubai, United Arab Emirates. ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3774904.3792737

## 1 Introduction

Phishing is a social engineering attack whereby adversaries impersonate legitimate entities to deceive users into divulging sensitive information (e.g., credentials, financial data), resulting in financial losses of approximately \$17,700 per minute [58]. Recognizing the severity of this threat, prior research has extensively studied the phishing ecosystem across multiple dimensions. Channel-based mechanisms have been examined, including email-based lateral phishing attacks [56], AI-enabled phishing generation and detection [54], SMS phishing [75], malicious Telegram activity [92], and phishing kits (packaged tools that lower barriers) [14, 76, 111].

However, these studies analyze phishing through post-attack data collection, examining deployed attacks, detection mechanisms, and victim-side defenses. This reactive approach provides insuficient visibility into emerging threats before they materialize into active attacks. Particularly, recent studies on underground ecosystems have examined dark web forums, characterizing anonymous marketplace growth [101], illicit revenue flows [79], duplicate phishing websites [115], and forum discussion dynamics [103]. While these studies provide valuable insights into illicit underground economies, they have not specifically examined the phishing supply chain, which is the mechanism by which phishing tools, techniques, and resources are disseminated and operationalized within the attacker communities.

To address this gap and characterize phishing threats from the attacker’s viewpoint, we examine D2Web forums where the phishing supply chain operates. These forums serve as both marketplaces and knowledge-sharing platforms where attackers acquire phishing tools (e.g., phishing kits), exchange Tactics, Techniques, and Procedures (TTPs), and trade compromised credentials [18]. By analyzing posts of the D2Web forums, we provide an attacker-centric characterization of phishing in terms of components, targets, and prices. To this end, we raise the following research questions:

• RQ1: Phishing Product Ecosystem. What phishing components (e.g., kits, infrastructure) are traded and shared on D2Web, and how are they utilized in phishing campaigns?

• RQ2: Temporal Dynamics. What are the distribution patterns and temporal trends of component and targeted services (e.g., financial institutions, email providers) revealed in forum?

• RQ3: Economic Structure. How are the prices of phishing components distributed across the underground marketplace?

To answer this, we first collect 394,034 posts from 13 D2Web forums between 2013 and 2025 (for 12 years). Given the vast volume of collected D2Web posts, we develop a LLM-based methodology to eficiently (1) identify phishing-related posts and (2) extract prod ucts and their attributes (e.g., price, target service). From these posts, we identify a total of 39 phishing components and map them to a seven-stage attack lifecycle derived from empirical case studies: 1 target list construction → 2 phishing site creation → 3 mali cious component creation → 4 infrastructure setup → 5 attack execution → 6 validation and refinement → 7 monetization.

Our analysis reveals distinct patterns across the phishing at tack lifecycle. In the 1 target list construction phase, posts related to valid target verification (particularly credential checkers) account for a high volume. Regarding target services, we observe phase-specific targeting patterns. Financial institutions (e.g., Pay Pal, banks) are primarily mentioned during the 2 phishing site creation phase, likely due to opportunities for direct monetary gain and credential theft. In contrast, the 3 malicious component creation phase predominantly targets platforms with large user bases, such as Discord and Steam. Notably, Steam-related activities exhib ited a marked increase during the COVID-19 pandemic, suggesting opportunistic targeting of services experiencing elevated usage. The economic characteristics of the underground market also vary by component type. Core components demonstrate varying price elasticity depending on functionality. During the 4 infrastructure setup phase, discussions of proxies for detection evasion maintain a consistent presence throughout the observation period.

We find that attacker concentration difers substantially across phases: while the top 10 contributors account for a small share of posts in most phases, the 2 phishing site creation phase shows that the top 10 authors responsible for 48% of posts. These findings provide a first attacker-centric longitudinal analysis of the phish ing supply chain over 12 years, highlighting its evolution and key dynamics. In summary, our contributions are as follows:

• We collect 394,034 posts from 13 D2Web forums over 12 years and analyze them with a newly designed LLM-based methodology to characterize the phishing underground.

• We identify 39 distinct phishing products within the underground ecosystem and map them to a seven-stage attack framework.

• Our analysis reveals trends on D2Web: Target List Construction (step 1 ) accounts for 73.45% of posts and targets large user base organizations and financial institutions. In Phishing Site Creation (step 2 ), the top 10 contributors account for 43% of posts, suggesting market concentration.

## 2 Background

Phishing Products. Phishing refers to an attack in which an adversary impersonates a legitimate entity and employs socialengineering techniques to induce user actions that result in a harm ful outcome [99]. Phishing can be characterized as a two-stage pro cess: impersonation and action inducement. Impersonation involves mimicking trusted entities (e.g., companies, government agencies) through oficial logos, deceptive domains, and forged sender names. To carry out phishing attacks, adversaries rely on various phishing products [55, 84, 97]. These products include datasets (e.g., leaked email addresses and phone numbers), tools (e.g., phishing kits that automatically generate phishing pages), and services (e.g., hackingfor-hire) that facilitate the execution of phishing campaigns. Prior studies [16, 18, 103] have shown that D2Web forums actively trade such malicious resources, including phishing products, enabled by the anonymity features of these networks.

Deep and Dark Web. The Web can be generally categorized into three types: the surface web, the deep web, and the dark web. The surface web comprises publicly accessible websites that can be indexed by search engines such as Google and Yahoo; however, it is estimated to represent only about 4% of the entire Internet [102]. The remaining resources reside on the deep and dark web (D2Web) [82, 115]. The deep web refers to online resources that are not collected or indexed by web crawlers, or are protected behind authentication and access control, making them inaccessible via typical search engines. Within this hidden space, the dark web represents an even more dificult-to-access subset that requires specialized tools such as the Tor and commonly relies on .onion domains. However, this anonymity has also contributed to illicit activities on the dark web[101], including the trade of hacking tools used in phishing attacks[49]. To gain a deeper understanding of the underground phishing ecosystem and emerging phishing strategies, this study investigates D2Web forums that ofer phishing products.

## 3 Methodology

This section outlines our methodology for analyzing the phishing ecosystem from an attacker’s perspective in underground markets. Overview. Figure 1 provides an overview of our methodology for analyzing posts from cybercrime forums on the D2Web over a 12-year period (2013–2025). We select 13 target forums based on dark web intelligence reports and the Tor hidden service directory, and collect posts using the ACHE crawler (Section 3.1). From 343,334 collected posts, we identify 70,055 phishing-related posts and extract phishing product information using a large language model (LLM). Details of the extraction process are provided in Section 3.2. We then construct a seven-stage phishing attack scenario (Section 4.1), map the extracted products to each stage, and analyze them to characterize the phishing ecosystem from an attacker’s perspective (Section 4.1, Section 4.2, and Section 4.3).

## 3.1 Data Collection

We first identify D2Web forums and collect cybercrime-related posts from the D2Web forums.

Target Forums Selection. We collect D2Web forums from two primary sources: (1) FreshOnion [107], a Tor hidden service directory, and (2) technical reports published by dark web intelligence companies. Following prior studies [66, 115], we extract 475 .onion domains of dark web forums from FreshOnion. To expand this list, we analyze publicly available reports from 28 well-reputed dark web intelligence companies [1, 2, 17, 19, 21, 26, 33–37, 39, 45– 47, 51, 63, 72, 74, 81, 85–88, 100, 104, 106, 113, 117], all of which actively provide dark web monitoring services [22, 32]. Figure 2 shows the number of posts collected from each dark web intelligence company. We then examine all reports of each company whose titles contain the keywords “deep web,” “dark web,” “dark net,” or “forum.” From 379 reports, we identify 88 D2Web forums and resolve their corresponding domains using the Ahmia search engine [3]. These steps yield a total of 556 unique D2Web forums: 475 forums from FreshOnion and 88 forums from the reports. We manually review all 556 candidate forums to verify their suitability for our research objectives. During our verification, forums are excluded for various reasons: 441 are inaccessible, 13 fail to resolve onion do main via Ahmia, 14 require logins incompatible with our crawler, 8 are non-English (Russian or German), 4 block registration, 2 require paid access and 33 are permanently closed. We additionally exclude 28 forums because they are not phishing related forums (e.g., drugs and cryptocurrency-laundering sites). Finally, 13 forums remain for phishing-related post collection: Crax.cc [29], Crax.pro [30], Altenens [7], Argo Market [68], Awazon [11], Breach Forum [20], Cracked.io [27], Cracking [28], Crax.shop [31], Stargate Market [71], King Market [69], Osiris Market [70], and Shadow X [114].

(a) Deep Web Forum  
![](images/3e8548c1d8c2e1f6303dc0332ef01cd4c686fa5cf00854e77438d8d7ab5f52f1.jpg)  
Figure 1: Overview of our methodology.

![](images/b1aaca87699fedd56bedf3285210a3c7990c07ed8f93a2dbfbcd620e4f48aa57.jpg)  
Figure 2: Number of posts collected from each dark web in telligence company.

![](images/55613d35e4196581169f81df3e5e5759b73cda4cc60c27e58449394527d7ac1b.jpg)  
Figure 3: An example of a real-world phishing post from the Altenens deep web forum ofering a phishing page.

D2Web Post Collection. We collect all posts from the 13 selected forums using the ACHE crawler [94]. We initially crawled 394,034 posts and obtained 343,334 unique posts after removing exact duplicates (identical titles and contents), covering approximately 12 years from April 2013 to August 2025. As illustrated in the example post from Altenens in Figure 3, each post contains a title, content, posting time, and author name. Since ACHE stores posts in HTML format, we pre-process the data to extract these fields and construct the final dataset used in our subsequent analysis.

Table 1: Number of posts collected per forum.

<table><tr><td>Forum</td><td>Post</td><td>(%)</td></tr><tr><td>Cracking</td><td>26,216</td><td>38.35%</td></tr><tr><td>Crackedio</td><td>23,219</td><td>33.96%</td></tr><tr><td>Altenen</td><td>15,750</td><td>23.04%</td></tr><tr><td>Crax.Pro</td><td>2,407</td><td>3.52%</td></tr><tr><td>Crax.shop</td><td>524</td><td>0.77%</td></tr><tr><td>Crax.cc</td><td>225</td><td>0.33%</td></tr><tr><td>Breachforum</td><td>24</td><td>0.04%</td></tr></table>

(b) Dark Web Forum

<table><tr><td>Forum</td><td>Post</td><td>(%)</td></tr><tr><td>Amazon Market</td><td>1,081</td><td>63.96%</td></tr><tr><td>King Market</td><td>240</td><td>14.20%</td></tr><tr><td>Stargate Market</td><td>139</td><td>8.22%</td></tr><tr><td>Shadow X</td><td>130</td><td>7.69%</td></tr><tr><td>Osiris Market</td><td>59</td><td>3.49%</td></tr><tr><td>Argo Market</td><td>41</td><td>2.43%</td></tr></table>

## 3.2 LLM-based Analysis for D2Web Posts

We employ a LLM to analyze the collected D2Web posts. Using its inference capability, we identify phishing-related posts and extract information about phishing product from the posts. In this study, we utilize the GPT-4o-mini model[80].

Identifying Phishing-related Posts. We apply two promptengineering strategies to identify phishing-related posts from 343k forum posts: Role-Play [98] and Specificity & Precision [116]. In the Role-Play prompt, the LLM is instructed to adopt the persona of a security analyst (“You are a security analyst.”) to ensure a consistent evaluative perspective. The Specificity & Precision technique minimizes ambiguity through explicit instructions and a structured output format. Posts directly or indirectly related to any stage of the phishing process are labeled 1, while unrelated posts (e.g., credit card fraud) are labeled 0. For borderline cases, we apply a strict rule: if a post could plausibly be used for phishing, it is labeled 1. The complete prompts are provided in Appendix (see Figure 9). As summarized in Table 1, using this method, the LLM identifies 70,055 phishing-related posts out of the 343k posts.

Extracting Phishing Product Information. To extract phishing product information from the identified phishing-related posts, we similarly adopt the Role-Play and Specificity & Precision prompting techniques. In the Role-Play prompt, the LLM is instructed to act as a D2Web forum user (“You are a dark web forum user.”) to interpret posts from the perspective of someone familiar with the forum’s internal discourse and slang (e.g., email:pass, combolist). The Specificity & Precision technique ensures that instructions and output formats are presented clearly to minimize ambiguity. Additionally, we incorporate a Few-Shot prompting strategy [23], providing concrete examples of phishing product information (e.g., product name, features) to improve extraction accuracy. The prompt is designed to extract four attributes of each product: product name, price, provided functionalities, and target service (e.g., Netflix, Gmail). The complete prompt is shown in Appendix (see Figure 10).

![](images/14c728eca15ef4f4054d1b6fac07fbaa6dbb25e6289b9962e4d343849b9ccf03.jpg)  
Figure 4: Seven steps of the phishing attack scenario with mapped phishing products extracted from D2Web posts.

Table 2: Identified phishing products and their categories.

<table><tr><td>Category</td><td>Phishing Product</td></tr><tr><td>Tool</td><td>Crawler, SQL Dumper, Account Creator, Number Creator, Account Checker, Email Checker, Editor, Checker Generator, Phishing Kit, Phishing Page, Binder, Crypter, RAT, HVNC, Spyware, Ransomware, Keylogger, Capture Tool, Clipper, Stealer, Malware, Proxy Checker, VPN Checker, Proxy Collector, Sender, Phone Spoofer, SEO Tool, Cookie Checker</td></tr><tr><td>Dataset</td><td>Credential, PII, Stealer Log</td></tr><tr><td>Service</td><td>Hosting Service, VPS, SSL Certification, Proxy, VPN, SMTP, BTC Mixer, Hacking-for-hire</td></tr></table>

Manual Verification of LLM Outputs. We manually verify the LLM’s outputs for two tasks: phishing post identification and phish ing product information extraction. For the phishing post identifica tion task, we randomly select 100 posts, and for product information extraction, 100 phishing-related posts, resulting in 200 samples in total. Two security researchers compare the LLM’s responses with the ground truth for validation. Evaluation metrics included precision $\begin{array} { r } { ( P = \frac { \mathrm { T P } } { \mathrm { T P + F P } } ) } \end{array}$ , recall $\begin{array} { r } { ( R = \frac { \mathrm { T P } } { \mathrm { T P + F N } } ) } \end{array}$ , and F1 $\begin{array} { r } { ( F _ { 1 } = \frac { 2 P R } { P + R } ) } \end{array}$ . For phishing post identification, TP, FP, and FN are defined based on whether the model correctly classifies a post as phishing or nonphishing. For product information extraction, we divide the task into two sub-tasks—product name extraction and service name extraction-each is evaluated independently using the same metrics. Because a post may contain multiple items, TP/FP/FN are based on whether the model identifies at least one correct product name or target service. GPT-4o-mini achieves precision 0.97, recall 0.84, and F1 0.90 for phishing-post identification. For product information extraction, it achieves precision 0.89, recall 0.88, and F1 0.89 for product name extraction, and precision 0.94, recall 0.83, and F1 0.88 for service name extraction, demonstrating high overall accuracy.

## 3.3 LLM Output Refinement

We normalize two elements extracted by the LLM: (1) product names and (2) target service names.

Product Name. Product names extracted by the LLM may in clude spelling variants, slang, and inconsistent expressions, causing multiple names to refer to the same functionality. We unify these variants into a single representative category. For example, account, credential, combo, and combolist refer to products providing credential information and are unified as credential products. In total, we collect 1,203 unique phishing product names. Through manual analysis and normalization, 329 names are consolidated into 36 categories, yielding 910 distinct phishing product names.

Target Service Name. Target services of the product also appear in varied formats (e.g., disney, disneyplus, disneyplus.com). We normalize them by mapping variants to the smallest token; for example, “disney”, “disneyplus”, and “disneyplus.com” are all mapped to “disney”. In total, we collect 11,889 unique target services. Converting them to lowercase removed case variants, reducing to 9,416. Applying smallest token mapping approach further merge 4,936 original forms into 980, resulting in 5,460 distinct target services.

Table 3: Post distribution across phishing scenario steps.

<table><tr><td>Step</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><td rowspan="2">Post (%)</td><td>62,853</td><td>193</td><td>1,422</td><td>8,670</td><td>164</td><td>12,273</td><td>1</td></tr><tr><td>73.45%</td><td>0.23%</td><td>1.66%</td><td>10.13%</td><td>0.19%</td><td>14.34%</td><td>0.00%</td></tr></table>

## 4 Results of Underground Ecosystem

We investigate the following three research questions.

## 4.1 RQ1. Phishing Product Ecosystem

Our goal is to understand which phishing products are traded on the D2Web and how they are used in real phishing campaigns. Phishing Attack Scenario. First, we develop a phishing campaign scenario by analyzing 30 real-world cases [4, 6, 12, 15, 24, 25, 38, 40– 44, 48, 50, 52, 53, 59–61, 67, 73, 77, 78, 89, 90, 95, 96, 108, 110, 119]. As shown in Figure 4, common phishing campaigns follow seven steps: 1 Target List Construction; 2 Phishing Site Creation; 3 Malicious Component Creation; 4 Infrastructure Setup; 5 Attack Execution; 6 Validation and Refinement; and 7 Monetization. We adopt this scenario model as the basis for addressing our RQ.

Phishing Products Identification. We manually analyze all 910 phishing products extracted via the LLM. For each product, we review its functionalities and map it to one of the seven phish ing attack steps in our scenario model. Two researchers perform the mapping and resolving disagreements through discussion; ultimately, 39 phishing products are assigned to a specific step (see Figure 4). The detailed descriptions of these products and their roles in each step are provided in Section A.1. These phishing products can be categorized into three types (see Table 2): Tools, Datasets, and Services. Tools comprise automated aids for phishing campaigns (e.g., phishing kits). Datasets include leaked data usable in attacks (e.g., user credentials). Services cover oferings that facilitate phishing operations (e.g., hacking-for-hire, phishing server hosting).

Phishing Products Distribution. 58,955 posts contain at least one of the 39 identified phishing products, and their distributions across the scenario steps is shown in Table 3. The total count exceeds 58,955 because a single post may correspond to multiple steps when it ofers more than one phishing product. Considering the overall 70,055 phishing-related posts, and excluding 4,431 posts that do not ofer phishing product, these 39 products account for approximately 90% of all phishing-related posts. Step 1 is dominant with 62,853 posts (73.45%), followed by Step 6 with 12,273 (14.34%) and Step 4 with 8,670 (10.13%). In contrast, Steps 2 , 3 , 5 , and 7 appear to be lower numbers. This distribution indicates that products related to infrastructure setup and target selection are shared more actively than those associated with attack execution.

![](images/e7df4b9d0b383103363f178237765643458285bb6551dc3606135483aa9bafd2.jpg)  
(a) Step 1

![](images/3b309a9dc6606cd1a0854ec4ddaa3f030688e8e29abda1dc0c78230eb886cfc3.jpg)  
(b) Step 2

![](images/8e86bc50d9055400a5ebd48d47b967684f886c04e86dff5d8f0454a07231873b.jpg)

![](images/54858939a76b24ccde5c231e5eece52b4f71c558ff6c18ada860d7f4668ecf24.jpg)

![](images/d61862c068ffa074d9051f7160d48bcbeea659a54403e1afdd2fb4c87a4725ea.jpg)  
(e) Step 5

(d) Step 4  
![](images/17260ef376b25d603a42702c6952cc7a732c973ad1c345f9b3fd4521b5af553b.jpg)  
(f) Step 6

(c) Step 3  
![](images/5d6e39f2601b9cdb264107cad3107af9f809246fee5b6d4ad0eb177d61be02f0.jpg)  
(g) Step 7

![](images/24fc53633ce492b0dc14d0872f16788f6250ceaa8d54c692efdeba59ed466f69.jpg)  
(h) Total  
Figure 5: Annual trends of phishing products (2013–2025) traded on underground markets across seven phishing steps.

Takeaway: Distribution of phishing products, concentrated in Steps 1 (73%), 4 (10%), and 6 (14%), highlighting greater activity in target selection and infrastructure preparation than in direct attack steps.

## 4.2 RQ2: Temporal Dynamics

We conduct a quantitative analysis of year-over-year trends in phishing products traded on D2Web.

Annual Trends of Phishing Products. Figure 5h shows the num ber of posts ofering phishing products from 2013 to 2025, revealing three major surges-in 2016, 2020, and 2023-that parallel increases in real-world phishing activity. We define a surge as a year-overyear increase of over 50%. In 2016, global phishing incidents rose by 65% year over year, reaching 1,220,523 in total, with 277,693 in the fourth quarter alone [8]. In 2020, activity surged again, begin ning in mid-March, with 165,772 phishing sites reported in the first quarter [9]. The 2023 data confirmed an all-time peak, with nearly five million incidents for the year and 1,077,501 in the fourth quar ter [10]. That same year, 21,489 business email compromise (BEC) cases and losses exceeding \$2.9 billion were reported, indicating record-high volume and impact [57]. Taken together, these findings suggest that posting trends on D2Web closely mirror real-world phishing activity. Accordingly, we examine step-level patterns to better capture the overall trajectory of phishing product evolution.

Takeaway: Phishing product posts on D2Web in 2013–2025 surged three times in 2016, 2020, and 2023, consistent with real-world indicators.

Annual Trends of Each Phishing Step. As shown in Figure 5a, Credential products attract the greatest interest, followed by Account Checker. This indicates that during the target list construction step ( 1 ), attackers primarily reuse leaked credentials and rely on checkers to validate large datasets. In the phishing site creation step ( 2 ), Phishing Pages that provide high-quality templates consistently outperform Phishing Kits (see Figure 5b). This suggests that attackers prefer constructing phishing sites using high-quality, ready-made phishing pages rather than relying on prepackaged kits. Moreover, as shown in Figure 5c, Capture Tools and Stealers dominate the top ranks in the malicious component creation step ( 3 ), followed closely by RATs. Since 2024, Stealers have overtaken Capture Tools, indicating a shift from screen-capture-based attacks to those centered on credential, session, and cookie theft. Overall, activity remains concentrated on information-gathering tools.

In the infrastructure setup step ( 4 ), Proxy and VPN products dominate, as depicted in Figure 5d. These tools provide features that periodically change IP addresses to evade detection, highlighting a strong demand for anonymity and persistence infrastructure. During the attack execution step ( 5 ), SMTP and Senders are actively traded (Figure 5e), reflecting the continued reliance on email-based delivery in phishing attacks. Indeed, over 3.4 billion phishing emails are reported to be sent daily as of 2025 [65]. Moreover, as of 2024, email remains the delivery vector in over 90% of breaches involving social engineering, including phishing [112]. These trends clearly demonstrate that email delivery remains a central pillar of the phishing ecosystem. As shown in Figure 5f, Account Checkers exhibit high demand during the verification and refinement step ( 6 ), reflecting the necessity of validating credentials prior to use. Freely shared account data often lacks reliability, whereas paid credentials typically include validity guarantees—making verification an essential part of attackers’ workflows. Finally, in the monetization step ( 7 ), we observe only BTC Mixer–related posts (see Figure 5g). This indicates that discussions about cash-outs or money laundering are minimal, suggesting that most underground activity remains focused on earlier steps of the phishing operation lifecycle.

![](images/0556a30e00b52ca7bffea51ebbeef3b0e96782bd0684cd58e3d8313afcb0972c.jpg)  
(a) Step 1

![](images/60f1f5bb77ccad4f77d8de838ea5c40b7e472a02e3e302b4b35296fceab28d9a.jpg)  
(b) Step 2

![](images/b6be706a3c878d5f509e53b4958735b417f42565bfa60017c48e66110bc1585e.jpg)  
(c) Step 3  
Figure 6: Major targeted services across the initial phishing steps. Attackers primarily focus on financial services (e.g., PayPal, Coinbase) and large-scale user platforms (e.g., Netflix, Discord), reflecting real-world shifts in service popularity.

Takeaway: Phishing products focus on Credential, anonymity via Proxy/VPN, and the use of ready-made phishing pages with email-based phishing (SMTP/Sender), while monetization remains minimal.

Annual Trends of Target Services. By analyzing the targeted services of phishing-related products, we investigate how attack ers’ focuses in phishing strategies evolve over time. We examine Steps 1 - 3 , which correspond to steps where attackers identify and prepare their victims. Figure 6a presents the targeted services in Step 1 . It shows the annual frequency of the top 20 targets extracted from leaked data provided by Credential, PII, Stealer Log, and Checker products (e.g., account or email checkers) that can be used to identify victims. We observe that companies with strong reputations and large customer bases are the primary targets, such as streaming platforms (e.g., Netflix, Spotify), payment services (e.g., PayPal), social networks (e.g., Facebook, Instagram), and on line games (e.g., Steam, Minecraft, Fortnite). Interestingly, Origin, a game distribution platform launched in 2011, was a major target between 2016 and 2021 but has been less targeted since 2022. This may be related to Origin discontinuing its Windows client in October 2022 [83], which likely reduced its user base. In contrast, Discord emerged as a frequent target beginning in 2020, coinciding with its surge in popularity during the COVID-19 pandemic [105]. Discord reported 140 million monthly active users in December 2020, up from 100 million in June 2020 [91]. These observations demonstrate that the trading trends on the D2Web closely reflects real-world shifts in user behavior and service popularity.

Figure 6b presents the targeted services used for phishing pages and kits in Step 2 . Phishing targets can be broadly categorized into two types: (1) financial services, which enable direct monetization, and (2) large-scale platforms, where attackers profit through infor mation theft and credential reuse. Approximately 45% of the targets are financial services, including banks (e.g., Chase Bank, Bank of America, Wells Fargo), payment platforms (e.g., PayPal), and crypto currency services (e.g., Coinbase, PancakeSwap, Trust, Crypto). This high proportion indicates attackers’ preference for services that enable direct monetary conversion. Beyond financial targets, other major categories include e-commerce (e.g., Amazon, eBay), streaming (e.g., Netflix, Spotify), gaming (e.g., Steam, Fortnite), and messaging platforms (e.g., Discord, Telegram). High-trafic platforms such as Facebook, LinkedIn, and Apple also remain frequent targets due to their large user bases and valuable authentication ecosystems. Netflix, in particular, began appearing as a phishing target on D2Web in 2018, coinciding with confirmed phishing incidents [109] and approximately 200 million credential stufing attempts against the platform [5]. It has been continuously targeted since then. The annual distribution also reveals temporal patterns in targeting. For instance, PayPal was heavily targeted during 2019–2020, while cryptocurrency services (e.g., Crypto, PancakeSwap, Trust, Coinbase) surged around 2023. These trends suggest adaptive attacker behavior, with phishing eforts dynamically shifting toward companies experiencing surges in user activity or financial transaction volume.

Similarly, financial services and platforms with large user bases are targeted by malware in Step 3 , as shown in Figure 6c. 20% are financial services (e.g., PayPal, Crypto, Bitcoin), while most of the remaining are high-user-volume platforms such as Discord, Instagram, and Steam. Discord exhibits a trend similar to Step 1 , showing an increase in targeting beginning in 2020, coinciding with its rapid growth during the COVID-19 pandemic. Steam also shows a strong upward trend from 2020 to 2024. In 2020, Steam reported significant growth, reaching 120 million monthly active users, and a peak of 24.8 million concurrent users [13], reflecting its continued prominence as a high-value target.

Takeaway: Phishing targets mirror real-world service trends, focusing on popular financial and high-user platforms like PayPal and Discord, reflecting attackers’ rapid adaptation to market dynamics.

Authors of Phishing Attacks. Table 4 shows the percentage of posts contributed by the top ten authors at each step. Step 2 (phishing pages/kits) shows the highest author concentration, with the top ten authors contributing 43% and the top author alone contributed 12.44%. In contrast, Steps 1 and 6 are more evenly distributed, where the top ten authors account for only 15.55% and 6.22%, respectively. This suggests a broadly distributed posting pattern, where many authors contribute small volumes of content rather than a few dominating the posting activity. Moreover, as shown in Table 4, top authors rarely share duplicate posts. Only three authors account for over 90% of duplicates, indicating that most top authors trade unique phishing products rather than repeatedly reposting the same content. We further analyze whether top authors post phishing products that correspond to diferent steps. As illustrated in Figure 7, top authors in Step 1 almost exclu sively post content from their own step. Similarly, Step 4 authors primarily post within their step. However, authors from other steps also frequently post Step 1 content, revealing a cross-step pattern where Step 1 products are widely shared by major contributors from other steps.

Table 4: Distribution of the top 10 authors by step. Share represents an individual author’s proportion of posts within each step, and Dup represents percentage of the author’s duplicate post rate by step. Total indicates the combined proportion of posts contributed by the top 10 authors in each step. Author names are intentionally masked with asterisks for ethical considerations.

<table><tr><td colspan="3">Step 1</td><td colspan="3">Step 2</td><td colspan="3">Step 3</td><td colspan="3">Step 4</td><td colspan="3">Step 5</td><td colspan="3">Step 6</td></tr><tr><td>Author</td><td>Share</td><td>Dup</td><td>Author</td><td>Share</td><td>Dup</td><td>Author</td><td>Share</td><td>Dup</td><td>Author</td><td>Share</td><td>Dup</td><td>Author</td><td>Share</td><td>Dup</td><td>Author</td><td>Share</td><td>Dup</td></tr><tr><td>Ghostl****r</td><td>3.68</td><td>15.89</td><td>GoldApp*****</td><td>12.44</td><td>0.00</td><td>NEWDAIS****D</td><td>10.02</td><td>0.00</td><td>vn5***k</td><td>8.18</td><td>30.61</td><td>thei****er</td><td>7.98</td><td>0.00</td><td>Ghostl****r</td><td>0.78</td><td>0.00</td></tr><tr><td>aka****5</td><td>2.89</td><td>11.61</td><td>both****d</td><td>9.33</td><td>0.00</td><td>Lee***N</td><td>4.77</td><td>14.71</td><td>shopsock****m</td><td>7.32</td><td>13.54</td><td>russi****g</td><td>3.07</td><td>60.00</td><td>bow**r</td><td>0.78</td><td>61.46</td></tr><tr><td>Immanu****t</td><td>1.50</td><td>2.34</td><td>spamming****t</td><td>4.66</td><td>0.00</td><td>Kor**N</td><td>3.01</td><td>93.02</td><td>@l3***@</td><td>2.40</td><td>23.08</td><td>0ve****w</td><td>2.45</td><td>0.00</td><td>RealMu****i</td><td>0.68</td><td>7.14</td></tr><tr><td>Agre****B</td><td>1.27</td><td>5.78</td><td>Neur****k</td><td>3.63</td><td>0.00</td><td>Poiso****s</td><td>2.59</td><td>13.51</td><td>wow****m</td><td>1.30</td><td>9.73</td><td>D**z</td><td>2.45</td><td>0.00</td><td>Ecl****N</td><td>0.68</td><td>6.02</td></tr><tr><td>FOR****N</td><td>1.23</td><td>14.29</td><td>Poiso****s</td><td>2.59</td><td>0.00</td><td>AlienT****e</td><td>1.61</td><td>0.00</td><td>Pias5P****1</td><td>1.18</td><td>11.76</td><td>Jen****o</td><td>2.45</td><td>0.00</td><td>na****1</td><td>0.68</td><td>97.59</td></tr><tr><td>FunDi****n</td><td>1.18</td><td>6.09</td><td>ausnarcosl****)</td><td>2.59</td><td>40.00</td><td>Wate****d</td><td>1.54</td><td>0.00</td><td>lun****y</td><td>1.18</td><td>12.75</td><td>Ban****B</td><td>1.84</td><td>0.00</td><td>ToFa****r</td><td>0.58</td><td>5.63</td></tr><tr><td>comb****a</td><td>1.14</td><td>17.04</td><td>russia****g</td><td>2.59</td><td>0.00</td><td>LMa**g</td><td>1.40</td><td>0.00</td><td>mash****8</td><td>1.10</td><td>4.21</td><td>Crac****O</td><td>1.84</td><td>0.00</td><td>Ha***_</td><td>0.54</td><td>3.03</td></tr><tr><td>renk****n</td><td>0.92</td><td>59.27</td><td>Papote****e</td><td>2.07</td><td>100.00</td><td>Ign****P</td><td>1.33</td><td>0.00</td><td>N*S</td><td>1.00</td><td>3.45</td><td>Lee****N</td><td>1.84</td><td>0.00</td><td>renk****n</td><td>0.51</td><td>76.19</td></tr><tr><td>ComboM****y</td><td>0.89</td><td>1.25</td><td>Jum****a</td><td>1.55</td><td>0.00</td><td>Mar***4</td><td>1.26</td><td>55.56</td><td>Po**r</td><td>0.98</td><td>8.24</td><td>Wi**n</td><td>1.84</td><td>0.00</td><td>DA****I</td><td>0.49</td><td>88.33</td></tr><tr><td>V01**e</td><td>0.85</td><td>35.39</td><td>iSYCO****i</td><td>1.55</td><td>0.00</td><td>24k***d</td><td>1.05</td><td>0.00</td><td>Sub***e</td><td>0.85</td><td>8.11</td><td>pu****e</td><td>1.84</td><td>66.67</td><td>Ma****4</td><td>0.49</td><td>33.33</td></tr><tr><td>Total</td><td>15.55</td><td></td><td>Total</td><td>43.00</td><td></td><td>Total</td><td>28.58</td><td></td><td>Total</td><td>25.49</td><td></td><td>Total</td><td>27.60</td><td></td><td>Total</td><td>6.21</td><td></td></tr></table>

![](images/d03a91c63df517bf8355a0489e247ce6345350ab95d60c8f75cdb0fb90d5ebee.jpg)  
Figure 7: Cross-step posting behavior between top authors and phishing products. S1–S7 Authors represent top authors in each step, and S1–S7 Products represent phishing products associated with each step.

Takeaway: Posting activity is broadly distributed among authors with few duplicates, and Step 1 content is often shared by top authors from other steps.

## 4.3 RQ3: Economic Structure

We analyze the average price of phishing products and the dif ferences between paid and free oferings.

Average Price of the Phishing Product. Figure 8 shows the av erage price of each phishing product category. Phishing pages and malware directly involved in malicious activities are traded at the highest prices. Other Malware refers to multi-function malware that is dificult to classify under a single function (e.g., a combination of a stealer and HVNC). These samples are multifunctional, often combining capabilities such as stealing credentials and remote access within a single package. Malware supporting multiple platforms are also more expensive; for example, variants compatible with both Windows and Android range from \$3,500 to \$10,000, which is higher than others. Phishing pages also show high prices due to their quality—many almost perfectly replicate legitimate websites, substantially increasing attack success rates. Overall, phishing products with features that improve attack efectiveness are valued more highly in underground markets.

![](images/6d1859ba3ed0538fc52d7f96170d64f7883419ed8dcef8792544cd3d5403b571.jpg)  
Figure 8: Average prices of phishing products traded on underground markets.

Takeaway: High-quality phishing pages and multifunctional, multi-platform malware that enhances attack efectiveness are traded at high prices.

Diferences Between Paid and Free Products. Products in Step 1 show clear distinctions between free and paid versions. Dataset products (PII, Credential, Stealer Log) contain similar information across both, but free datasets lack validity guarantees. Tools such as Account Creator, Account Checker, Editor, and Crawler provide core functionality for free, while paid versions ofer faster, proxyenabled verification to prevent blocks from excessive login attempts. Hacking Services are always paid and can be leveraged when leaked data cannot be obtained elsewhere. In Step 2 , phishing-page prices vary by sophistication: free pages generally mimic only login pages, while paid ones replicate multi-page, highly realistic sites, substantially increasing attack success. For malware in Step 3 , functional diferences appear minimal, as the same malware names and ver sions (e.g., RedLine, Mars) are ofered in both paid and cracked posts and their described functionalities are largely identical; paid versions mainly difer by providing regular updates and user support (e.g., guidelines, Q&A). Infrastructure services such as proxy and VPS in Step 4 are typically ofered as free trial versions, which do not guarantee large-scale data processing or long-term reliability. Attack with Free Products. We observe that most phishing prod ucts are freely available, with few exceptions, including Hacking Services, phishing pages for crypto platforms (e.g., crypto.com), and malware targeting specific exchanges (e.g., Coinbase). Aside from these cases, all services listed in Figure 6 are supported by free products, allowing attackers to perform the full seven steps phishing attacks using only freely available underground products. As discussed above, free products have limitations, but attackers can combine multiple free tools to overcome them. For example, leaked datasets lack validity guarantees but can be verified using free Account Checkers. Missing target data can be generated by using an Editor to create email lists from domain variants and vali dating them with an email checker. Likewise, free proxy trials can be collected with proxy scrapers and filtered with proxy checkers to maintain long-term proxy access at no cost.

Takeaway: Most phishing products are free, and their limitations can be overcome by combining multiple products.

## 5 Discussion & Limitation

Phishing Attack Scenario. We design a seven-step phishing attack scenario from the attacker’s perspective, based on 30 real world cases, providing a generalized representation that may not capture all attack variations. Nevertheless, this framework is sufi ciently comprehensive to map all 39 identified phishing products and address our research questions.

Outputs from an LLM. Identifying phishing posts and extracting phishing product information using the LLM has inherent accuracy and reliability limitations. It is prone to hallucination, producing false outputs when post content is ambiguous. We do our best efort to mitigate issues through manual verification and prompt engineering optimization, achieving approximately 90% accuracy. Selected D2Web Forums. Our study is based on 13 forums, which may appear limited. However, these forums are identified as major platforms by prominent dark web intelligence companies. The dataset, comprising 343,334 posts collected over 12 years, provides a solid foundation for large-scale and longitudinal analysis.

Collected Dataset. Our dataset is limited to English-language deep and dark web forums. As a result, our findings may be biased toward English-speaking marketplaces and may underrepresent phishing ecosystems operating in other languages (e.g., Russianlanguage or Chinese-language communities).

## 6 Related work

Several prior studies have investigated the phishing ecosystem and trends in underground markets.

Phishing Ecosystem. The phishing ecosystem has been widely studied across channels, phishing kits, and websites/URLs. Channel based research covers lateral phishing, AI-generated emails, SMS phishing, and Telegram-based cybercrime via DarkGram [54, 56, 75, 92]. Investigation of phishing kits has examined server-side filtering, evasion and obfuscation, and end-to-end kit lifecycle [14, 76, 111]. Website and URL analysis has also been studied , including largescale client-side cloaking, network-based URL inference, and hybrid and deep URL classifiers [62, 64, 93, 118]. Unlike prior studies, we analyze phishing across the full operational scenario and examine the D2Web phishing ecosystem from the attacker’s perspective.

Underground Ecosystem. Prior research on the underground ecosystem focuses on online forums, including measuring ecosystem growth [101], estimating illicit revenue through Tor crawling and clustering [79], analyzing 21 million Tor webpages to identify phishing domains targeting major dark web and gray services [115], and studying discussion topics, temporal trends, and cross-forum links to detect anomalous activity [103]. In contrast, our work focuses on phishing products ofered on D2Web to characterize their features, examine how they can be used in phishing attacks

## 7 Conclusion

This study presents the first longitudinal analysis of phishing ecosystem from the attacker’s perspective on the deep and dark web. Using the LLM-based analysis, we examine 343,334 posts collected over 12 years from 13 major D2Web forums, identifying 39 distinct phishing products and mapping them to a seven-stage phishing attack framework. Our findings show that attackers heavily rely on credential products and high-quality phishing pages, with financial and high-user-volume services being the most targeted. While most products are freely available, attackers can efectively combine them to construct end-to-end phishing campaigns. Overall, our results provide empirical insights into the operational structure, evolution, and economic characteristics of the underground phishing ecosystem, forming a foundation for proactive threat intelligence and defense strategies.

## Acknowledgments

We thank the anonymous reviewers for their constructive feedback. This work was partly supported by the three Institute of Information & Communications Technology Planning & Evaluation (IITP) grants funded by the Korean government (MSIT; Ministry of Science and ICT) (No.2024-00337703; Development of satellite security vulnerability detection techniques using AI and specificationbased automation tools, No.2024- 00398745; Proofs and responses against evidence tampering in the new digital environment, No. 2022-0-00688; AI Platform to Fully Adapt and Reflect Privacy-Policy Changes, IITP-2025-RS-2024-00437849; ICT Challenge and Advanced Network of HRD, No. RS-2025-25457342: Development of Scale-out Cloud that Interconnects Micro Data Centers, and No. RS-2025-25394739: Development of Security Enhancement Technology for Industrial Control Systems Based on S/HBOM Supply Chain Protection). Additional support was provided by the National Science Foundation under awards CNS-2440819 and DGE-2335798. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the sponsor.

## References

[1] Intel 471. 2014. Darkweb intelligence firm: Intel 471. https://www.intel471.com/ [2] ACID. 2014. Darkweb intelligence firm: ACID. https://www.acid-tech.com/

[3] Ahmia. 2025. Ahmia: Tor Hidden Service Search Engine. https://ahmia.fi/.

[4] AhnLab ASEC. 2019. Distribution and Operation of Malware ’Crypter’ Exploit ing Malicious Spam. ASEC Blog. https://asec.ahnlab.com/en/16500/

[5] Akamai. 2019. Streaming Services Among the Most Targeted by Credential Stufing Attacks According to Akamai Report. https://www.akamai.com/newsr oom/press-release/state-of-the-internet-security-credential-stuffing-attacks and-economies

[6] Jan Michael Alcantara. 2024. Phishing with Cloudflare Workers: Transparent Phishing and HTML Smuggling. https://www.netskope.com/blog/phishingwith-cloudflare-workers-transparent-phishing-and-html-smuggling

[7] Altenens. 2008. Altenens website. https://altenens.is/

[8] Anti-Phishing Working Group (APWG). 2017. Phishing Activity Trends Report, 4th Quarter 2016. https://docs.apwg.org/reports/apwg\_trends\_report\_q4\_2016 .pdf

[9] Anti-Phishing Working Group (APWG). 2020. Phishing Activity Trends Report, 1st Quarter 2020. https://docs.apwg.org/reports/apwg\_trends\_report\_q1\_2020 .pdf

[10] Anti-Phishing Working Group (APWG). 2024. Phishing Activity Trends Report, 4th Quarter 2023. https://docs.apwg.org/reports/apwg\_trends\_report\_q4\_2023 .pdf

[11] Awazon. 2020. Awazon. http://awazonhndi7e5yfaobpk7j2tsnp4kfd2xa63tdtzcg 7plc5fka4il4ad.onion/

[12] Tom Barnea. 2025. Ongoing Campaign Abuses Microsoft 365’s Direct Send to Deliver Phishing Emails. https://www.varonis.com/blog/direct-send-exploit

[13] Ekaterina Bespyatova. 2021. 120 million monthly active users and 31.3 billion game hours — Steam summed up the results of 2020. https://app2top.com/anal ytics/120-million-monthly-active-users-and-31-3-billion-game-hours-steamsummed-up-the-results-of-2020-180149.html

[14] Hugo Bijmans, Tim Booij, Anneke Schwedersky, Aria Nedgabat, and Rolf van Wegberg. 2021. Catching phishers by their bait: Investigating the dutch phishing landscape through phishing kit detection. In 30th USENIX security symposium (USENIX security 21). 3757–3774.

[15] Vaibhav Billade. 2025. Spear Phishing Campaign Delivers VIP Keylogger via Email Attachment. Seqrite Technical Blog. https://www.seqrite.com/blog/spearphishing-campaign-delivers-vip-keylogger-via-email-attachment/

[16] Alex Biryukov, Ivan Pustogarov, Fabrice Thill, and Ralf-Philipp Weinmann. 2014. Content and popularity analysis of Tor hidden services. In 2014 IEEE 34th International Conference on Distributed Computing Systems Workshops (ICDCSW). IEEE, 188–193.

[17] Bitsight. 2011. Darkweb intelligence firm: Bitsight. https://www.bitsight.com/

[18] BOLSTER. 2024. Zero to Hero of Phishing: Modern Phishing Attacks by Lever aging Dark Web Tools and AI. https://bolster.ai/blog/zero-to-hero-of -phishingmodern-phishing-attacks-by-leveraging-dark-web-tools-and-ai

[19] Brandefense. 2018. Darkweb intelligence firm: Brandefense. https://brandefens e.io/

[20] BreachForums. 2022. Breach Forums. https://breachforums.info/

[21] Breachsense. 2018. Darkweb intelligence firm: Breachsense. https://www.brea chsense.com/

[22] BREACHSENSE. 2024. The 10 Best Dark Web Monitoring Services. https: //www.breachsense.com/blog/best-dark-web-monitoring-services/

[23] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. In Advances in Neural Information Processing Systems 33 (NeurIPS). Curran Associates, Inc., 1877–1901.

[24] Jenny Chen. 2025. Cybersecurity Stop of the Month: Adversary-in-the-Middle Attacks that Target Microsoft 365. https://www.proofpoint.com/us/blog/email and-cloud-threats/aitm-phishing-attacks-evolving-threat-microsoft-365

[25] CISA. 2017. Google Docs Phishing Campaign (US-CERT Alert). https://www.ci sa.gov/news-events/alerts/2017/05/04/google-docs-phishing-campaign

[26] CorwdStrike. 2011. Darkweb intelligence firm: CrowdStrike. https://www.cr owdstrike.com/ko-kr/

[27] Cracked.io. 2018. Cracked.io. https://cracked.io

[28] Cracking. 2018. Cracking. https://cracking.org/

[29] Crax.cc. 2025. Crax.cc. https://crax.cc/ Deep Web Forum ； Year based on WHOIS creation date: 2025-09-06.

[30] Crax.pro. 2020. Crax.pro. https://crax.pro/

[31] Crax.shop. 2022. Crax.shop. https://crax.shop

[32] CRYPTIKA. 2025. 10 Best Dark Web Monitoring Tools in 2025. https://www.cr yptika.com/10-best-dark-web-monitoring-tools-in-2025/

[33] CTM360. 2014. Darkweb intelligence firm: CTM360. https://www.ctm360.com

[34] Cybelangel. 2013. Darkweb intelligence firm: CybelAngel. https://cybelangel.c om/

[35] Searchlight Cyber. 2017. Darkweb intelligence firm: Searchlight Cyber. https: //slcyber.io/

[36] Cyberint. 2010. Darkweb intelligence firm: Cyberint. https://cyberint.com/ [37] Cyble. 2019. Darkweb intelligence firm: Cyble. https://cyble.com

[38] Alexandre Côté Cyr. 2024. Life on a Crooked RedLine: Analyzing the Infamous Infostealer’s Backend. https://www.welivesecurity.com/en/eset-research/lifecrooked-redline-analyzing-infamous-infostealers-backend

[39] darkowl. 2016. Darkweb intelligence firm: DarkOwl. https://www.darkowl.com/

[40] Graham Edgecombe. 2024. Phishception – SendGrid is abused to host phishing attacks impersonating itself. https://www.netcraft.com/blog/popular-emailplatform-used-to-impersonate-itself

[41] ENKI WhiteHat Team. 2025. Analysis of FormBook Payload Loaded by Pure-Crypter Distributed from South Korean IP. https://www.enki.co.kr/en/mediacenter/blog/analysis- of- formbook- payload- loaded- by- purecrypterdistributed-from-south-korean-ip

[42] Europol. 2023. One of the Darkweb’s Largest Cryptocurrency Laundromats Washed Out (ChipMixer). https://www.europol.europa.eu/media-press/news room/news/one-of-darkwebs-largest-cryptocurrency-laundromats-washedout

[43] Harry Everett. 2024. Out ofthe Shadows — ’darcula’ iMessage and RCS Smishing Attacks Target USPS and Global Postal Services. https://www.netcraft.com/blo g/darcula-smishing-attacks-target-usps-and-global-postal-services

[44] Harry Everett. 2025. AI-Enabled Darcula-Suite Makes Phishing Kits More Accessible, Easier to Deploy. https://www.netcraft.com/blog/ai-enableddarcula-suite-makes-phishing-kits-more-accessible-easier-to-deploy

[45] Flare. 2017. Darkweb intelligence firm: Flare. https://flare.io/

[46] Flashpoint. 2010. Darkweb intelligence firm: Flashpoint. https://flashpoint.io/ [47] Foresiet. 2020. Darkweb intelligence firm: Foresiet. https://foresiet.com

[48] Fortra Suspicious Email Analysis Team. 2024. Cloudflare’s pages.dev and workers.dev Domains Increasingly Abused for Phishing. https://www.fortra.com/b log/cloudflare-pages-workers-domains-increasingly-abused-for-phishing

[49] Jason Franklin, Adrian Perrig, Vern Paxson, and Stefan Savage. 2007. An inquiry into the nature and causes of the wealth of Internet miscreants. In In Proceedings of the 2007 ACM Conference on Computer and Communications Security (CCS). 375–388.

[50] GOV.UK. 2021. Avoid and Report Internet Scams and Phishing. https://www. gov.uk/report-suspicious-emails-websites-phishing

[51] Group-IB. 2003. Darkweb intelligence firm: Group-IB. https://www.groupib.com/

[52] Group-IB Threat Intelligence. 2022. Roasting 0ktapus: The Phishing Campaign Going After Okta. https://www.group-ib.com/blog/0ktapus/

[53] Group-IB Threat Intelligence. 2024. Phishy Business: Unraveling LabHost’s scam ecosystem. https://www.group-ib.com/blog/labhost-operation

[54] Fredrik Heiding, Bruce Schneier, Arun Vishwanath, Jeremy Bernstein, and Peter S Park. 2024. Devising and detecting phishing emails using large language models. IEEE Access 12 (2024), 42131–42146.

[55] Shane Hickey. 2025. UK student jailed for selling phishing kits linked to £100m of fraud. https://www.theguardian.com/technology/2025/jul/24/canterburystudent-phishing-kits-jailed-fraudsters

[56] Grant Ho, Asaf Cidon, Lior Gavish, Marco Schweighauser, Vern Paxson, Stefan Savage, Geofrey M Voelker, and David Wagner. 2019. Detecting and characterizing lateral phishing at scale. In 28th USENIX security symposium (USENIX security 19). 1273–1290.

[57] FBI Internet Crime Complaint Center (IC3). 2023. 2023 Internet Crime Report. https://www.ic3.gov/annualreport/reports/2023\_ic3report.pdf

[58] SSL Insights. 2025. Phishing Statistics for 2025: Latest Figures and Trends. https://sslinsights.com/phishing-statistics

[59] Microsoft Threat Intelligence. 2023. DEV-1101 Enables High-Volume AiTM Campaigns with Open-Source Phishing Kit. https://www.microsoft.com/enus/security/blog/2023/03/13/dev-1101-enables-high-volume-aitm-campaignswith-open-source-phishing-kit

[60] Mimecast Threat Intelligence. 2025. Direct Send Abuse. https://www.mimecast .com/threat-intelligence-hub/microsoft-direct-send-abuse

[61] Matt Kapko. 2025. Infostealers Fueled Cyberattacks and Snagged 2.1B Creden tials Last Year. https://cyberscoop.com/infostealers-cybercrime-surged-2024- flashpoint/

[62] Abdul Karim, Mobeen Shahroz, Khabib Mustofa, Samir Brahim Belhaouari, and S Ramana Kumar Joga. 2023. Phishing detection system through hybrid machine learning based on URL. IEEE Access 11 (2023), 36805–36822

[63] KELA. 2009. Darkweb intelligence firm: KELA. https://www.kelacyber.com/

[64] Taeri Kim, Noseong Park, Jiwon Hong, and Sang-Wook Kim. 2022. Phishing URL detection: a network-based approach robust to evasion. In Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security (CCS). ACM, 1769–1782.

[65] Keepnet Labs. 2024. 250+ Phishing Statistics and Trends You Must Know in 2025. https://keepnetlabs.com/blog/top-phishing-statistics-and-trends-youmust-know

[66] Seunghyeon Lee, Changhoon Yoon, Heedo Kang, Yeonkeun Kim, Yongdae Kim, Dongsu Han, Sooel Son, and Seunghwon Shin. 2019. Cybercriminal minds: an investigative study of cryptocurrency abuses in the dark web. In 26th Network

and Distributed System Security Symposium (NDSS). The Internet Society.

[67] Pei Han Liao. 2025. SEO Poisoning Attack Targets Chinese-Speaking Users with Fake Software Sites. https://www.fortinet.com/blog/threat-research/seopoisoning-attack-targets-chinese-speaking-users-with-fake-software-sites

[68] Argo Market. 2023. Argo Market. http://argo4y7i55eafmunecspkroynos76c7p x7l6or3cdbpekltxqlxqjmqd.onion

[69] King Market. 2021. King Market. http://kingl5yq6n3h5b6bsc3ut7uytjdecvla3j bmhcofu4nzsogoap2oqnid.onion

[70] Osiris Market. 2025. Osiris Market. http://osirisdaec7ufbb3sbe3r355b2s7lwvw 726l4z4oumg6kdddnomht3qd.onion Year based on first archived snapshot of Tor Link listing (Wayback, 2025-08-09)

[71] Stargate Market. 2025. Stargate Market. http://emskd5wz645mvyadsfhcomuw uj3j32ejy6jcqhmcepno3dboyqze2pyd.onion Year based on archived snapshot of Tor Link listing (archive.md/XLUuO).

[72] MCS. 1984. Darkweb intelligence firm: MCS. https://www.micromindercs.co m/dark-web-monitoring-threat-intel-solutions

[73] Microsoft Defender Experts. 2023. Detecting and Mitigating a Multi-Stage AiTM Phishing and BEC Campaign. https://www.microsoft.com/en-us/security/blog /2023/06/08/detecting-and-mitigating-a-multi-stage-aitm-phishing-and-beccampaign/

[74] Munit. 2016. Darkweb intelligence firm: Munit. https://munit.io/

[75] Aleksandr Nahapetyan, Sathvik Prasad, Kevin Childs, Adam Oest, Yeganeh Ladwig, Alexandros Kapravelos, and Bradley Reaves. 2024. On SMS phishing tactics and infrastructure. In 2024 IEEE Symposium on Security and Privacy (SP). IEEE, 1–16.

[76] Adam Oest, Yeganeh Safei, Adam Doupé, Gail-Joon Ahn, Brad Wardman, and Gary Warner. 2018. Inside a phisher’s mind: Understanding the anti-phishing ecosystem through phishing kit analysis. In 2018 APWG Symposium on Electronic Crime Research (eCrime). IEEE, 1–12.

[77] U.S. Department of Justice. 2023. Justice Department Investigation Leads to Takedown of Darknet Cryptocurrency Mixer (ChipMixer). https://www.just ice.gov/archives/opa/pr/justice-department-investigation-leads- takedowndarknet-cryptocurrency-mixer-processed-over-3

[78] U.S. Department of the Treasury. 2022. U.S. Treasury Sanctions Notorious Virtual Currency Mixer Tornado Cash. https://home.treasury.gov/news/pressreleases/jy0916

[79] Kris Oosthoek, Mark van Staalduinen, and Georgios Smaragdakis. 2023. Quan tifying dark web shops’ illicit revenue. IEEE Access 11 (2023), 4794–4808.

[80] OpenAI. 2024. GPT-4o mini. https://openai.com/index/gpt-4o-mini-advancingcost-efficient-intelligence/

[81] Outpost24. 2001. Darkweb intelligence firm: Outpost24. https://outpost24.com/

[82] Steve Pederson. 2013. White paper: Understanding the Deep Web in 10 minutes

[83] Jay Peters. 2022. EA’s new PC app is here to replace Origin. https://www.thever ge.com/2022/10/7/23392775/ea-new-pc-app-launcher-replace-origin-macos

[84] Deerendra Prasad. 2025. Threat Spotlight: A million phishing-as-a-service attacks in two months highlight a fast-evolving threat. https://blog.barracuda .com/2025/03/19/threat-spotlight-phishing-as-a-service-fast-evolving-threat

[85] Prescient. 2008. Darkweb intelligence firm: Prescient. https://prescient.com/da rk-web-intelligence

[86] Rapid7. 2000. Darkweb intelligence firm: Rapid7. https://www.rapid7.com/

[87] Recorded. 2009. Darkweb intelligence firm: Recorded. https://www.recordedfu ture.com/

[88] ReliaQuest. 2007. Darkweb intelligence firm: ReliaQuest. https://reliaquest.com

[89] SOCRadar Research. 2025. Stealer Logs: Everything You Need to Know. https: //socradar.io/stealer-logs-everything-you-need-to-know/

[90] Mark Risher. 2017. Protecting You Against Phishing. https://security.googleblo g.com/2017/05/protecting-you-against-phishing.html

[91] Discord Safety. 2021. Discord Transparency Report: July — Dec 2020. https: //discord.com/blog/discord-transparency-report-july-dec-2020

[92] Sayak Saha Roy, Elham Pourabbas Vafa, Kobra Khanmohammadi, and Shirin Nilizadeh. 2024. DarkGram: a large-scale analysis of cybercriminal activity channels on Telegram. arXiv preprint arXiv:2409.14596 (2024).

[93] Ozgur Koray Sahingoz, Ebubekir BUBE, and Emin Kugu. 2024. Dephides: Deep learning based phishing detection system. IEEE Access 12 (2024), 8052–8070.

[94] Aécio Santos, Kien Pham, Deepti Verma, Juliana Freire, Aron Ahmadia, Tommy Ellqvist, Ayman Abdel Ghany, Jonathan Leitschuh, Jeongkyu, Yamuna Krishna murthy, and Christine Doig. 2025. ache. https://github.com/VIDA-NYU/ache

[95] Alexandra Sentenac. 2025. MFA Under Attack: AiTM Phishing Kits Abusing Legitimate Services (Tycoon 2FA). https://www.darktrace.com/blog/mfaunder-attack-aitm-phishing-kits-abusing-legitimate-services

[96] U.S. Postal Inspection Service. 2025. Smishing: Package Tracking Text Scams. https://www.uspis.gov/news/scam-article/smishing-package-tracking-textscams

[97] Tim Kromphardt Jake Gionet Shachar Gritzman, Moshe Avraham and Eilon Bendet. 2023. Cloud Account Takeover Campaign Leveraging EvilProxy Targets Top-Level Executives at over 100 Global Organizations. https://www.proofpoi nt.com/us/blog/email-and-cloud-threats/cloud-account-takeover-campaignleveraging-evilproxy-targets-top-leve

[98] Murray Shanahan, Kyle McDonell, and Laria Reynolds. 2023. Role play with large language models. Nature 623, 7987 (2023), 493–498.

[99] Multi-State Information Sharing and Analysis Center (MS-ISAC). 2023. Phishing Guidance: Stopping the Attack Cycle at Phase One. https://www.cisa.gov/sites /default/files/2023-10/Phishing%20Guidance%20-%20Stopping%20the%20Atta ck%20Cycle%20at%20Phase%20One\_508c.pdf

[100] SocRadar. 2019. Darkweb intelligence firm: SocRadar. https://socradar.io/

[101] Kyle Soska and Nicolas Christin. 2015. Measuring the longitudinal evolution of the online anonymous marketplace ecosystem. In 24th USENIX security symposium (USENIX security 15). 33–48.

[102] Jabeen Sultana and Abdul Khader Jilani. 2021. Exploring and analysing surface, deep, dark web and attacks. Security Incidents & Response Against Cyber Attacks (2021), 85–96.

[103] Nazgol Tavabi, Nathan Bartley, Andres Abeliuk, Sandeep Soni, Emilio Ferrara, and Kristina Lerman. 2019. Characterizing activity on the deep and dark web. In Companion Proceedings ofthe 2019 World Wide Web Conference (WWW’19 Companion). 206–213.

[104] Teamt5. 2017. Darkweb intelligence firm: Teamt5. https://teamt5.org/en/

[105] TheLance. 2021. The Rise of Discord Among Students During the COVID-19 Pandemic. https://www.thelance.ca/2021/09/27/the-rise-of -discord-amongstudents-during-the-covid-19-pandemic/

[106] ThreatMon. 2018. Darkweb intelligence firm: ThreatMon. https://threatmon.io/

[107] Torlink. 2020. Torlink. https://tor.link/site/dig-ai/info Tor Hidden Service Directory; Year based on WHOIS creation date: 2020-11-297.

[108] Bill Toulas. 2022. Google SMTP Relay Service Abused for Sending Phishing Emails. https://www.bleepingcomputer.com/news/security/google-smtp-relayservice-abused-for-sending-phishing-emails

[109] Colleen Tressler. 2022. Netflix phishing scam: Don’t take the bait. https://cons umer.f tc.gov/consumer-alerts/2018/12/netflix-phishing-scam-dont-take-bait

[110] UltraViolet Cyber (UVCyber). 2024. Sendception: SendGrid Impersonation Campaign. https://www.uvcyber.com/hubfs/downloadable-content/product% 2Dsheets/Sendception%20-%20SendGrid%20Impersonation%20Campaign.pdf

[111] Andrea Venturi, Michele Colajanni, Marco Ramilli, and Giorgio Valenziano Santangelo. 2022. Classification of Web Phishing Kits for early detection by platform providers. arXiv preprint arXiv:2210.08273 (2022).

[112] Verizon. 2024. 2024 Data Breach Investigations Report. https://www.verizo n.com/business/resources/reports/2024-dbir-data-breach-investigationsreport.pdf

[113] Web-IQ. 2011. Darkweb intelligence firm: Web-IQ. https://www.web-iq.com/

[114] Shadow X. 2025. Shadow X. http://shadowxn3o3kvvkbjyaoe33emqxrtadijp7x ybizbht2thb6x5dvfhad.onion Year based on first archived snapshot of onion.live listing (Wayback, 2025-05-19);

[115] Changhoon Yoon, Kwanwoo Kim, Yongdae Kim, Seungwon Shin, and Sooel Son. 2019. Doppelgängers on the dark web: a large-scale assessment on phishing hidden web services. In Companion Proceedings ofthe 2019 World Wide Web Conference (WWW ’19 Companion). 2225–2235.

[116] Shakhzod Yuldoshkhujaev, Mijin Jeon, Doowon Kim, Nick Nikiforakis, and Hyungjoon Koo. 2025. A Decade-long Landscape of Advanced Persistent Threats: Longitudinal Analysis and Global Trends. arXivpreprintarXiv:2509.07457 (2025).

[117] ZeorFox. 2013. Darkweb intelligence firm: ZeroFox. https://www.zerofox.com/

[118] Penghui Zhang, Adam Oest, Haehyun Cho, Zhibo Sun, RC Johnson, Brad Wardman, Shaown Sarker, Alexandros Kapravelos, Tifany Bao, Ruoyu Wang, et al. 2021. Crawlphish: Large-scale analysis of client-side cloaking techniques in phishing. In 2021 IEEE Symposium on Security and Privacy (SP). IEEE, 1109–1124.

[119] Xiaopeng Zhang. 2024. Deep Analysis of Snake Keylogger’s New Variant. https://www.fortinet.com/blog/threat-research/deep-analysis-of-snakekeylogger-new-variant

## A Appendix

## A.1 Details of Phishing Products

Step 1 : Target List Construction. The products that can be used in this process are various. Credentials are authentication information used to login (e.g., usernames, passwords). Personally Identifiable Information (PII) refers to information that can identify an individual (e.g., name, passport number, address, phone number). A stealer log is the consolidated output of information-stealing malware, typically containing cookies, credentials, PII. A crawler is a program that automatically collects targeted content (e.g., credential, PII) from web pages (e.g., d2web forum). An SQL dumper is a tool or script that exports large volumes of database records as a dump file. Hacking service is when a hacker carries out an attack on a specified target on someone’s behalf. The number generator is a tool that automatically generates a virtual phone number, and the account generator is a tool that automatically registers an account on an online site or randomly creates an creadential. An account checker is a tool that tests large sets of accounts to identify valid lo gins. An email checker is a tool that verifies, at scale, whether email addresses exist and can receive messages. Editor is a data-shaping tool that transforms data from one format to another and removes unwanted records. For example, it can convert mail:password pairs into user:password by dropping the email domain, and it can prune lists by deleting invalid accounts. Using product, an attacker can construct a target list. Attackers compile target lists using collected credentials, PII, and stolen logs. Automated tools such as crawler, SQL dumper, account creator, and number generator can further expand accounts, email addresses, and phone numbers. Email check ers and account checkers are then used to validate the collected data. Finally, an editor is used to remove duplicates, normalize formats, and standardize fields to produce the final target list.

Step 2 : Phishing Site Creation. Attackers create fake web sites (e.g., a gmail login page) that appear genuine to deceive people. Phishing pages and kits can be used for this purpose. A phishing page is a webpage that mimics the appearance of a legitimate site, while a phishing kit is a tool package containing such pages along with necessary files and configurations. Some phishing kits also support creating the desired phishing page. Most sellers on the forum only provide pages and kits, but some sellers also ofer ser vices that support hosting and operation if the attacker pays an additional fee. Using these products, attackers build a phishing site that mimics a legitimate target.

Step 3 : Malicious Product Creation. Some phishing attacks infect the target with malware via web pages or attachments. A binder is a tool that combines a benign-looking file with a malicious payload so they appear as a single file. A crypter is an obfuscation or encryption wrapper applied to malware to evade detection by security solutions. A RAT is malware that provides remote control of an infected system. Hidden VNC is a technique or tool that opens a concealed virtual desktop session to remotely operate the browser or system without the user’s knowledge. Spyware is malware that covertly collects and transmits user activity, screen content, or communications. Ransomware is malware that encrypts or locks files or systems and demands payment for restoration. A keylogger is malware that records and transmits keystrokes, which can directly expose passwords and payment information. A capture tool is software used to record and collect on-screen content. A clipper is malware that replaces sensitive clipboard values—such as cryptocurrency wallet addresses—with attacker-controlled values. A stealer is malware that broadly exfiltrates sensitive information, including browser cookies, sessions, passwords, and wallet seed phrases. Other Malware is a general term for software designed to cause harm, exert unauthorized control, or steal information. A binder combines payloads with documents or executables. A crypter applies packing and obfuscation to evade detection. Malware such as RATs, HVNC, spyware, and ransomware enables initial compro mise and remote control. Keyloggers, capture tools, clipper, and stealers exfiltrate user input and sensitive information.

Step 4 : Infrastructure Setup. Attackers can set up infrastruc ture using various services and tools. Hosting services rent out servers to host websites. If this infrastructure is abused, phishing pages can be distributed to appear as legitimate sites. A Virtual Private Server (VPS) is a form of virtualization that uses virtualization to partition a physical server into multiple independent virtual servers. Additionally, VPS in forums refers to services that provide VPS. In other words, it means renting an independent virtual server through virtualization. SSL certificate verifies the identity of a server or domain and enables encrypted HTTPS communication. This often leads users to mistakenly believe it is secure due to the browser’s lock icon. A proxy is a server that relays data between a client and a server. By using this proxy, the actual IP address can be hidden, displaying the proxy server’s IP address instead, thereby protecting the user’s identity. Such proxies are provided as a service that rents out servers. A VPN is a private networking technology used to encrypt data and hide the user’s IP address. In the D2Web forums, a VPN refers to a service that leases and provides access to use a VPN. A proxy collector is a tool that aggregates publicly available proxy lists from various sources. A proxy checker is a tool that verifies whether collected proxies are operational and evaluates their properties. A VPN checker is a tool that tests whether a given VPN can successfully connect and function. Attackers first rent server resources through hosting services or VPS to build infrastructure for their attacks. They then connect a domain and SSL certificate to set up HTTPS, upload phishing page files to the server, and make them accessible online. SAfter that, they use proxies and VPNs to build an environment to avoid detection. Public proxy lists are gathered via scrapers and checked for connectivity, speed, anonymity, and location using checkers. If necessary, VPN checkers are also used to test the proper functioning of specific VPN endpoints. During the operational phase, proxies are periodically rotated to avoid blacklists, concealing the origin and extending the campaign’s lifespan.

Step 5 : Attack Execution. Attackers can use sender, Simple Mail Transfer Protocol (SMTP), phone spoofers, and SEO tools to deliver phishing attack-related content. Sender is not an individual but a system that composes and sends bulk emails/texts. It constructs sender names/addresses, subject lines, body text, links, and attachments for queuing and transmission, providing performance metrics like bounce rates, opens, and clicks via a dashboard. SMTP is the standard protocol for email transmission, and a SMTP server executing this protocol handles the actual sending. Therefore, sending emails externally ultimately requires a SMTP server. The forum ofers a service that rents out SMTP servers, which can be used either through a free trial or a paid subscription. Additionally, attacker can send emails using Sender, which provides SMTP infrastructur. A phone spoofer is a tool that manipulates the caller ID displayed on the recipient’s screen during calls or texts. It is used to spoof the sender’s number or name, confusing trust. SEO tool is software designed to boost search visibility. It elevates the ranking of phishing sites or hosted files in search results, making them appear legitimate and potentially confusing users. In actual campaigns, senders and SMTP are used to mass-send diverse messages containing content (e.g., links, and attachments). In phone/SMSbased scenarios, phone spoofing makes them appear as legitimate institutions to induce clicks or responses. Additionally, SEO tools can boost phishing sites’ search rankings, creating access points via search paths. This enables attackers to use multiple channels simultaneously, employing various routes to reach victims.

Step 6 : Validation and Refinement. This step verifies data obtained during execution. A cookie checker is a tool that tests whether a browser cookie remains valid for browser cookie. In formation (e.g., email, credential, cookie) are tested with email checkers, account checkers, and cookie checkers to assess validity. Validated data are then curated with an editor to remove duplicates, standardize formats, and normalize fields for downstream misuse.

Step 7 : Monetization. The final step converts stolen assets into profit. A BTC mixer is a service that blends cryptocurrency transactions to impede tracing of their origin and flow. Attackers sell exfiltrated data on forums or leverage compromised accounts for secondary gains. BTC mixers are used to reduce the traceability of funds. These services split and recombine transactions across multiple wallets to obscure provenance. This step completes the economic objective of the campaign.

## A.2 Prompts Used for Analysis

```txt
You are a security analyst. Your task is to classify whether a given forum post is related to phishing.

0. Strict Rule
You should consider it phishing if there is some room for it to be used in phishing attacks.
The final output must be strictly in JSON format with only two fields: {"label": 0 or 1, "filename": "<exact input file name>"}

1. Phishing classification
Posts that are directly or indirectly related to phishing attack are considered to be associated with phishing attacks and are therefore assigned label 1. Posts directly or indirectly related to the entire process of a phishing attack consider the label to be 1.

2. Non-phishing
Posts about other forms of fraud, such as credit card fraud, are labeled as 0 if phishing is not mentioned.

3. Output Format
The final output must be strictly in JSON format with only two fields: {"label": 0 or 1, "filename": "<exact input file name>"}

The meaning of each label is as follows:
- 0 = Non-phishing (unrelated post)
- 1 = Phishing-related (related post)
```  
Figure 9: Identifying phishing-related post.

```txt
You are a darkweb forum user. Your task is extracting product information from forum's post.

1. Product information
If the post mentions any product (e.g., tool, proxylist, account, information, pii, etc.) or service (e.g., proxy, vpn), extract them. Do not confuse a product with the objective for which the product is used. Objectives should be recorded in the features fieldid.

Multiple products may be present, so return them as an array. For each product, extract:
- name: Product type only without target
    ex) account, proxy, combo, vpn, config, checker,
    combolist, login access, editor, email-pass, email:pass,
    socks5, ssl, phishing page, scam page, scampage,
    phishing page, phishing kit, phishing tool, guideline,
    stealer, ransomeware, malware, capture tools, log,
    cookie, tutorial
- price: Price of product
    ex)"\$30", "9.99 usd", "free", "$10-\$50"
- features: a brief phrase of explicitly stated capabilities/attributes.
- target: the target brand/service
    ex) "gmail", "netflix", "ms365", "trust wallet"

2. Output Format
The final output must strictly follow the JSON structure below.
If product aren't mentioned, it is labeled as "non-existence".
If there are multiple products or services, they should all be derived as a list.

When products exist, return:
{"products": [{"name": "<output name>", "price": "<price info or null>", "features": "<features or null>", "target_service": "<target service or null>"}], "filename": "<filename>"}
```  
Figure 10: Extracting phishing product information.

## A.3 Ethical Considerations

This study was conducted in strict compliance with ethical and legal standards. We did not download any data via download links, file-sharing links, archive links, or similar means within forum posts to avoid collecting or storing illegally obtained credentials or PII posted on the forums. During the dark web crawling process, we took care to avoid exposure to content that should not be accessed, specifically preemptively blocking the possibility of collecting highrisk content (e.g., illegal pornography). To this end, we collected only text data via the crawler and did not collect or store non-text media such as images, videos, or compressed files. The collected text is used solely for aggregation and analysis for research purposes. We did not attempt any actions that would compromise the anonymity of data subjects (e.g., re-identification) and did not participate in illegal transactions or pay for access.