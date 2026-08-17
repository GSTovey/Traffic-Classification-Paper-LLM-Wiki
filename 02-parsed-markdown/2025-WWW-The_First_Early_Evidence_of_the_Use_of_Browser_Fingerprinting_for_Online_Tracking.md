# The First Early Evidence of the Use of Browser Fingerprinting for Online Tracking

Zengrui Liu Nanjing University of Finance and Economics Nanjing, China Texas A&M University College Station, Texas, United States lzr@nufe.edu.cn

Jimmy Dani Texas A&M University College Station, Texas, United States danijy@tamu.edu

Yinzhi Cao Johns Hopkins University Baltimore, Maryland, United States yzcao@cs.jhu.edu

Shujiang Wu F5.Inc Seattle, Washington, United States sh.wu@f5.com

## Abstract

While advertising has become commonplace in today’s online in teractions, there is a notable dearth of research investigating the extent to which browser fingerprinting is harnessed for user track ing and targeted advertising. Prior studies only measured whether fingerprinting-related scripts are being run on the websites but that in itself does not necessarily mean that fingerprinting is being used for the privacy-invasive purpose of online tracking because fingerprinting might be deployed for the defensive purposes of bot/fraud detection and user authentication. It is imperative to ad dress the mounting concerns regarding the utilization of browser fingerprinting in the realm of online advertising.

This paper introduces “FPTrace” (fingerprinting-based tracking assessment and comprehensive evaluation framework), a framework to assess fingerprinting-based user tracking by analyzing ad changes from browser fingerprinting adjustments. Using FP-Trace, we emulate user interactions, capture ad bid data, and mon itor HTTP trafic. Our large-scale study reveals strong evidence of browser fingerprinting for ad tracking and targeting, shown by bid value disparities and reduced HTTP records after fingerprint ing changes. We also show fingerprinting can bypass GDPR/CCPA opt-outs, enabling privacy-invasive tracking.

In conclusion, our research unveils the widespread employment of browser fingerprinting in online advertising, prompting critical considerations regarding user privacy and data security within the digital advertising landscape.

## CCS Concepts

• Computing methodologies → Modeling and simulation; • Security and privacy;

Nitesh Saxena Texas A&M University College Station, Texas, United States nsaxena@tamu.edu

Measurement studies of privacy issues, Privacy policies, Web privacy

ACM Reference Format: Zengrui Liu, Jimmy Dani, Yinzhi Cao, Shujiang Wu, and Nitesh Saxena. 2025. The First Early Evidence of the Use of Browser Fingerprinting for Online Tracking. In Proceedings ofthe ACM Web Conference 2025 (WWW ’25), April 28-May 2, 2025, Sydney, NSW, Australia. ACM, New York, NY, USA, 16 pages. https://doi.org/10.1145/3696410.3714548

## 1 Introduction

Browser fingerprinting is a technique employed to surreptitiously collect data regarding a user’s web browser settings during their online activities. The collected data is then utilized to construct a unique digital identity, commonly referred to as a ‘fingerprint,’ for that specific user browser. Each time a user visits a website, there is potential for the site to employ browser fingerprinting as a means to identify or track the user. Many earlier research studies, such as Englehardt et al. [25] and Lerner et al. [32] and reports such as [4], assumed that the adoption of a fingerprinting script itselfis an indication ofweb tracking and a violation ofweb privacy. However, this assumption does not hold — just like cookies, browser fingerprinting can be used for defensive security purposes, like bot/fraud detection or authentication. For example, Wu et al. [45] show that adversarial fingerprints are diferent from those of benign users and therefore many real-world websites are using fingerprints for bot/fraud detection. As another example, Lin et al. [33] have demonstrated the real-world usage of browser fingerprinting in authentication just like what Laperdrix et al. [29] have illustrated in a feasibility study.

Therefore, the research question that we are answering in this paper is: whether browser fingerprints are indeed adopted for online tracking, thus violating web privacy. To the best of our knowledge, none of the prior works have established the link between browser fingerprinting and online tracking. On one hand, many works [25, 32], as mentioned above, consider the existence of fingerprinting scripts as a means of online tracking, which is not true. On the other hand, people have studied the relationship between personalized advertisements and web tracking in general, like cookie-based tracking. For instance, Wills et al. [44] explored ad tracking on the Google and Facebook advertising platforms. Similarly, Zeng et al. [47] employed header bidding to assess targeted ads. These studies did not specifically address the methods employed to link tracking with online advertising; therefore, it re mains unclear whether browser fingerprinting contributes to online tracking and privacy violation.

This paper seeks to bridge this gap in current research and regu latory assessment practices by investigating whether advertising ecosystem indeed utilizes browser fingerprinting for user tracking and targeting via a measurement study. Our key insight is that if browser fingerprinting plays a role in online tracking, the change of fingerprints will also afect the bidding of advertising and the un derlying HTTP records. Specifically, our approach involves leaking user interest data through controlled A/B experiments, modifying browser fingerprints, and leveraging advertiser bidding behavior and HTTP events as a contextual indicator in the advertising ecosys tem to deduce changes in advertisements. Given that advertiser bidding behavior and HTTP events are influenced by their prior knowledge of the user, we anticipate notable changes in this infor mation when altering browser fingerprints.

Our Contributions: We ofer the first study to measure whether browser fingerprinting is being used for the privacy-invasive pur poses of user tracking, targeting and advertising. Our main contributions can be summarized as follows:

(1) We introduce a framework, FPTrace, for detecting changes in advertisements following alterations in browser fingerprinting. FPTrace simulates real user interactions, captures advertiser bids, records HTTP data, and removes or exports cookies to observe such changes for the measurement of purposes of browser fingerprints.

(2) Our findings provide evidence that browser fingerprinting is indeed utilized in advertisement tracking and targeting. The bid value dataset exhibits notable diferences in trends, mean values, median values, and maximum values after changing browser fingerprints. Moreover, the number of HTTP records, encom passing HTTP chains and syncing events, decreases significantly after altering browser fingerprints. We also evaluate the role of browser fingerprinting in cookie restoration. Our results confirm that certain cookies contain browser fingerprinting information. We documented 378 instances of cookie restoration related to fingerprinting across 90 unique combinations of cookie keys and host pairs across all settings. However, there is no conclusive evidence to support browser fingerprinting’s direct involvement in cookie restoration after we did the manual inspection.

(3) We further study the potential malicious use of fingerprinting in the presence of data protection regulations such as GDPR and CCPA when used with content management platforms. Even under the GDPR and CCPA regulation protections, there are significant variations in the number ofHTTP chains and syncing events observed in certain instances when browser fingerprints are altered. Under GDPR, websites utilizing Onetrust, Quantcast, and NAI might be involved in data sharing activities that use browser fingerprinting to identify users. Under CCPA, Onetrust, and NAI might be involved in data sharing activities that use browser fingerprinting to identify users.

## 2 Background

## 2.1 Browser Fingerprinting

Browser fingerprinting is a technique to identify users using data collected from browsers, which may be unique to each browser (we refer to [30] for a representative survey in browser fingerprinting).

Yen et al. [46] and Nikiforakis et al. [39] assess the eficacy of fingerprinting techniques. Vastel et al. [43] examine the discrepancies present in browser fingerprints. Boda et al. [20] and Cao et al. [21] investigate alternative aspects of browser fingerprinting. Previous studies have explored various facets of browser fingerprinting, including techniques involving canvas [36], JavaScript [37], and hardware [38] methods. Information like User Agent which contains the users’ browser version and operating system version can be obtained by the website via HTTP header. Screen resolution, canvas fingerprints, users’ current time zone information can be accessed by the website via JavaScript APIs. Such information can be gathered and used to construct a user profile. Eckersley [24], Fifield et al. [26] and Laperdrix et al. [31] have shown that the browser fingerprints can be used for user identification due to their uniqueness. Acar et al. [19] and Iqbal et al. [28] demonstrated that browser fingerprints can be utilized in fraud detection. In real-world appli cations, services like Datadome [7], Radware [8], and HUMAN [16] employ browser fingerprinting for the purpose of fraud detection. Previous research such as [41] and articles like [4] solely assessed the presence of fingerprinting-related scripts on websites. However, this alone does not indicate malicious intent for user tracking.

Website “COVER YOUR TRACK” can display each browser fingerprint feature [6]. Website “AM I UNIQUE” can also show the uniqueness of each browser fingerprint among all other users [13]. Website “FingerprintJS” generate a unique ID for each user by using the browser fingerprints, and also display the ID to user [3].

## 2.2 Browser Fingerprint Spoofing

Spoofing browser fingerprints enables the concurrent operation of multiple browser instances on a single device, each with distinct browser fingerprinting. The Gummy Browser poses a significant threat to the privacy and security of applications that rely on browser fingerprinting [35]. This tool employs three distinct methods of attack, script injection, script modification, and the exploitation of the browser’s inherent settings and debugging tools. Notably, the Gummy Browser exhibits the capability to successfully emulate all JavaScript-based browser fingerprinting techniques, including the sophisticated canvas fingerprinting method. In script modification, the attacker wields the ability to manipulate the behavior of the JavaScript API “toDataURL()” by substituting it with either a predefined or randomized string. Conversely, in the case of script injection, the attacker can strategically introduce a breakpoint within the script precisely at the juncture where the JavaScript API “toDataURL()” is invoked, thereby enabling the replacement of its value with either a predetermined or random string.

## 2.3 Cookie Restoration

Cookies play a crucial role in recognizing devices, such as computers, within a network. Some cookies are designed to pinpoint individual users, enhancing their web browsing experience. When these cookies are deleted or expire, cookie restoration becomes valuable for reinstating them. Users have the option to safeguard their cookies for potential restoration by employing extensions that export cookies to JSON files or by manually copying cookie data from their browser profiles in case of accidental deletion. On the other hand, websites may endeavor to retain cookies within users’ browsers and restore them even after users have deleted the cookies, thereby maintaining user tracking capabilities.

## 2.4 Header Bidding

Header bidding [10] is a method employed by publishers on web sites. Here, publishers designate specific advertising spaces for po tential advertisers. The advertiser securing the highest bid gains the chance to display their ads in the corresponding slots. In client-side header bidding, users have the convenience of directly accessing and observing all the bids from their web browsers. Prebid.js [15] is a notable implementation of header bidding. Through the API pbjs.getBidResponses(), users on the client side can inspect the list of advertisers who engaged in bidding process to secure the oppor tunity to display ads during the current user’s visit. In the study outlined in [40], the author observes that profiles classified as “Only category” command prices around 40% higher than those assigned to “New user” profiles. The key finding underscores that advertisers’ bidding behavior is shaped by their prior familiarity with the user, resulting in elevated bid values compared to users for whom advertisers lack previous knowledge. Liu et al. [34] additionally demonstrated that advertisers with knowledge of users through data syncing tend to submit higher bid values in header bidding.

## 2.5 Privacy Regulations

Recently, the European Union introduced the General Data Protection Regulation (GDPR) [1], and California introduced the Cali fornia Consumer Privacy Act (CCPA) [2], both possessing the potential to regulate and restrain the online advertising and tracking ecosystem. GDPR requires that online services secure user consent (Articles 4 (11)) prior to processing user data (Article 6 (1) (a)). CCPA requires online services to ofer users the ability to opt-out of the sale of their personal data (Section 1798 (a) (1)). Both require websites to provide privacy notices containing information and controls for opting in/out of the collection and processing of per sonal information, which should include browser fingerprints. To comply with these requirements, websites are required to integrate consent management platforms (CMPs) [18]. CMPs scan websites, identifying all cookies set by HTTP headers and scripts from first and third-party resources. In the case of GDPR, CMPs must ensure that only necessary cookies are shared, and consent is obtained before sharing non-essential cookies. In the case of CCPA, CMPs should ensure that they provide users with controls to opt-out of the sale of personal information.

## 3 FPTrace: Our Framework to Assess Fingerprinting Use in Tracking

## 3.1 Framework Design

The objective of this research is to explore the utilization of finger printing in the realms of cookie restoration and targeted advertising.

To achieve this, it is imperative to design a robust framework tailored for eficient data acquisition. Given the limitations of manual data collection, our proposed framework “FPTrace” is engineered to automate this process.

FPTrace is capable of emulating human user behavior by systematically visiting a curated list of websites categorized under specific keywords, such as “Computer". During the visit, FPTrace not only loads the website but also simulates the behavior of a real human user by browsing the webpage. It is capable of clicking on various links or advertisements, moving the mouse to specific areas on the webpage, and even interacting with functions provided by third-party services, such as Consent Management Platforms (CMPs) or standard cookie banners. After exploring the websites, FPTrace is able to compile a browser profile, encompassing details like browsing history and cookie data. This comprehensive profile is designated as the “Interest Persona”, serving as a representation of user interests and preferences. Furthermore, it has the capability to extract data directly from advertisers, facilitating an in-depth analysis of targeted advertising triggers. FPTrace is capable of capturing and recording data such as bidding behaviors from various advertisers, as well as personal data syncing events. This information is then securely stored within the local database of FPTrace.

The design ensures versatility by allowing the FPTrace to sequentially or concurrently access multiple websites. Additionally, FPTrace is equipped to export and compare cookies after a stipulated number of website visits. To enhance its relevance in the domain of fingerprinting, integrated features have been incorporated for browser fingerprinting spoofing.

## 3.2 Framework Implementation

We present the tools we utilized in the FPTrace framework and the functions we implemented to meet the varying requirements of our experiments.

3.2.1 Web Crawling. We used OpenWPM [25] to construct our crawling FPTrace. OpenWPM is a widely used tool to collect large amount ofdata related to privacy. OpenWPM relied on the Selenium [17] to handle browser Firefox to do automated crawling.

OpenWPM has default functionality for browsing a list of websites, saving and loading browser profiles, and recording HTTP data. However, our experiments require further parameters. We added functionality to the OpenWPM to gather bid information.

For collecting bids, we used the Prebid.js, a popular implementation of the header bidding protocol [15], mostly because it takes place on the client side, enabling us to intercept the bidding process [5]. The bids objects we get from Prebid.js include all partipated advertisers information, and the ads image HTML contents.

We have incorporated a feature that allows the removal of all cookies from the browser profile. This function ensures that the process of data training and collection is completed automatically, free from any influence by human behaviors.

While gathering data through web crawling, we integrated functionality to mimic typical human behaviors. FPTrace enables the simulation of mouse movement from the top to the bottom of web pages, accompanied by scrolling down, and introduces random waiting periods ranging from 1 to 10 seconds. This feature enhances the realism of the crawler’s interaction with the website, resembling genuine human browsing behavior.

3.2.2 Spoofing Browser Fingerprints. Our experiments require the use of diferent browser fingerprints. We implemented an extension to spoofJavaScript based browser fingerprints features.

By spoofing JavaScript APIs, we used real browser fingerprints data from an dataset on Github [42]. The data is collected from real devices. In spoofing JavaScript APIs, we used Script Injection code provided by Gummy Browser [35] to overwrite all possible JavaScript APIs that can be used in browser fingerprints, such as Navigator(API: Navigator), Screen(API: Screen), Canvas(API: canvas.getContext) and Date(API: Date) APIs. To ensure the spoofing of all APIs prior to the loading of any webpage, we encapsulated all spoofing scripts within a browser extension.

Only spoofing JavaScript APIs may not work if websites match the value from JavaScripts to the one from HTTP header. So we have also spoofed the HTTP header. ModHeader [12] is an extension to allow users to modify HTTP headers. We embedded Selenium ModHeader [11] version into OpenWPM to spoof HTTP header.

3.2.3 Capturing Bidding Object. Header bidding can signal the enthusiasm of potential bidders. A bidder interested in showcasing their advertisements in the present slot will typically place higher bids. Cook et al. [23] have proved that the header bidding can be used to identify if the user is tracked. A higher bid can represent the user is tracked, and the user information is used by publishers, bidders, or bidding auctions. Specifically, we use Prebid.js to monitor bidders’ behaviors. Prebid.js is an implementation of header bidding protocol, and the user can get bidders’ behaviors, including the winner of each ad slot, the ads image HTML contents, and also all of the participated bidders bids value.

OpenWPM does not have functions to record bidding behaviors, so we inject codes to record those behaviors when the crawlers browse the website with Prebid.js and displaying ads.

3.2.4 Exporting Cookies. Grasping the significance of browser fin gerprints in advertising also necessitates an examination of cookie data. Fingerprints could become crucial if cookies that were deleted get reinstated. OpenWPM currently lacks functionality for export ing complete cookie data after each website visit by the crawler, or after visiting a random selection of websites. Therefore, we have developed a function that allows for the export of all cookies, both first and third-party, accumulated in the browser managed by Open WPM, regardless of the circumstances.

## 4 Measurement Study Methodology

In this section, our measurement study methodology that utilizes the FPTrace framework is introduced. Initially, in Section 4.1, we outline the simulation of interest personas, which emulate real person’s interests. Following this, in Section 4.2, the collection of bids and HTTP data using various settings is presented, employing simulated interest personas to visit websites that use Prebid.js. Subsequently, the detection of cookie restoration post removal is discussed in Section 4.3, followed by an elaboration on the identification of browser fingerprinting-associated cookie restoration in Section 4.4. Figure 1 provides an overview of the measurement study methodology. Finally, in Appendix A.3, the configuration for discerning whether browser fingerprinting persists for data collection post-user opt-out under GDPR and CCPA protection is discussed.

![](images/cd00f67cf2f35091464e2a6ebcc5a308107ed3374f9bd44d008f4cab3f2cd8ef.jpg)  
Figure 1: High level overview ofmeasurement study methodology. In Step 1, We create browser persona by visiting a list of websites. This step is called “Simulating Interest Personas”. In Step 2, we first use trained persona to visit websites which display ads, then collect bids and HTTP data. This step is called “Collecting Bids and HTTP Data”. In Step 3, we extract cookies from the browser profile and compare them between diferent experiment settings. This step is called “Detecting Cookie Restoration”. In Step 4, we analyze the manual inspect extracted cookies. This step is called “Detecting Fingerprinting Related Cookie Restoration”.

## 4.1 Simulating Interest Personas

A Persona encapsulates key attributes of a real individual, encompassing aspects such as personal interests, characteristics, and traits. Likewise, Browser Personas serve to embody the browsing preferences of web users, encompassing factors like desired purchases, vacation destinations, and preferred news topics. Websites and third-party services seek to understand, track, and tailor personal advertisements to users, making Browser Interest Personas invaluable in this endeavor. To understand how advertisers perform bidding based on users’ interests, it is essential to simulate browsers with specific interests before engaging in Prebid.js auctions for displaying ads. We begin by compiling a list of websites, denoted as $W _ { p } ,$ within a particular topic. Alexa provides topic-specific website lists, but not all are closely related to the topic keywords. To address this, we employ Google search to construct distinct website lists. We select the first 40 websites from the search results and manually inspect them to eliminate duplicates.

Once we have compiled the website list $W _ { p } ,$ we need to bypass web driver detection, as OpenWPM uses Selenium for automation. This involves overwriting the JavaScript API Navigator.webdriver, which distinguishes between real user visits and automation.

Subsequently, we direct OpenWPM to sequentially visit websites from $W _ { p } ,$ . After visiting the last website on the list, we save the browser profile. This profile, denoted as $P _ { \boldsymbol { p } } ,$ represents a simulated persona with an interest in the specific topic. This is Step 1 (A1, A\*1, B1) in Figure 2. We present various fingerprinting configurations in the browser extension. When the framework initializes, it will either load the spoofed fingerprints or not, depending on the specific settings. This ensures the framework can operate automatically under diferent configurations. All settings will activate simultaneously. It should be noted that the websites in Step 1 are visited sequentially. Step 1 and Step 2 for diferent configurations A1, A\*1, B1, A2, A\*2, B2 are run in parallel. The websites in Step 1 are listed in Appendix A.1. The websites in Step 2 are listed in Appendix A.2

![](images/41b105b8bdbd67315fc4f68aae0ebf3a75ca42cf26ced3b8b53c8809ca2cffa3.jpg)  
Figure 2: High level overview of advertisement experiment. In step 1, FPTrace will visit websites sequentially to keep updating the browser profile. In Step 2, FPTrace will control the browser with updated profile to visit each website. In Step 3, FPTrace will record the bids data and HTTP data. In Step 4, FPTrace will not update the current browser profile, and load the profile updated after Step 1. After visiting all websites in Step 2, FPTrace will compare the bids data and HTTP data between A, A\* and B.

## 4.2 Collecting Bids and HTTP Data

To collect bids data and investigate factors afecting bid behavior under the same browser profile, we first establish a data collection website list, $W _ { b i d s }$ . We create a detector to visit the Alexa top 10,000 websites list. Functions are developed to identify websites utilizing the Header Bidding implementation tool Prebid.js. The default API, pbjs, facilitated by Prebid.js, furnishes bidding data from various advertisers. Upon detection of Prebid.js during a website visit and successful retrieval of bidding records via the pbjs API, the website is flagged. Subsequently, all flagged websites are stored in the list $W _ { b i d s } .$ After assembling the list, we use the $P _ { p }$ profile to visit $W _ { b i d s }$ Step 2 (A2, A\*2, B2) in Figure 2 represents the process. After we gathering bid data and HTTP data from the Step 3 (A3, A\*3, B3) in Figure 2, we can do the analysis to measure the targeting. The updated profile will remain the same during Step 2 and Step 3. This could eliminate of the efects from the previous visited websites in Step 2. In Step 3 (A3, A\*3, B3) depicted in Figure 2, it is im portant to highlight that we extend our consideration beyond just the winning bid to encompass all advertising participants. Even if these participants did not secure the bid, their bids still ofer valu able insights into their interest in the current visitor. Therefore, we carefully collect and consider their bids as part of our methodology.

To explore the impact of browser fingerprinting on bid changes, we first use the true browser fingerprints in experiments A and A\*, which are represented in Figure 2. It should be noted that the updated profiles in A and A\* are diferent. We do not use the same profile for the diferent experiment, even the settings are all the same. We also have another experiment, which is denoted as B in Figure 2. In this setting, we replace the true browser fingerprint by using a brand new spoofed fingerprint.

![](images/45c7cf597147c16efea7b0d3855a85d95ec68d566d937e24ffb48103cc29b794.jpg)  
Figure 3: High level overview ofcookie restoration experiment. In Step 1, FPTrace will control the browser to visit websites. In Step 2, FPTrace will export all cookies including including 1st party and 3rd party cookies. In A and A\*, FPTrace will use the same browser fingerprints, and same experiment conditions. In B, FPTrace will use a diferent browser fingerprint. Then FPTrace will do cookie comparisons between A, A\* and B.

Table 1: Various configurations involving browser profiles, cookies, browser fingerprinting, and IP addresses.

<table><tr><td>Setting Number</td><td>New Profile?</td><td>Have Cookies?</td><td>True Fingerprint?</td><td>True IP?</td></tr><tr><td>a</td><td>Yes</td><td>No</td><td>Yes</td><td>Yes</td></tr><tr><td>b</td><td>No</td><td>Yes</td><td>Yes</td><td>Yes</td></tr><tr><td>c</td><td>No</td><td>Yes</td><td>No</td><td>Yes</td></tr><tr><td>d</td><td>No</td><td>No</td><td>Yes</td><td>Yes</td></tr><tr><td>e</td><td>No</td><td>No</td><td>No</td><td>Yes</td></tr></table>

## 4.3 Detecting Cookie Restoration

Our next step is to examine cookie restoration under various settings. In the "True Setting" $( S _ { t r u e } )$ , which is represented as A in Figure 3, we initiate a new browser profile without any pre-existing data, including browsing history and cookies. By using the Open-WPM framework to load the browser profile, and sequentially visit a list of websites, the profile is updated after each visit. The resulting profile is termed $P _ { t r u e }$ , and the exported cookie from profile $P _ { t r u e }$ is designated as $C _ { t r u e }$

Following this, we erase all data, including browsing history and cookies, from the browser profile. Initially, we unzip the browser profile, remove all data associated with history and cookies, and subsequently zip the remaining files to generate the new browser profile. To ensure thorough data removal, we opt for creating a new browser profile instead of using $P _ { t r u e }$ . This new profile, labeled $P _ { 0 }$ is employed to visit the same websites as in $S _ { t r u e }$ while operating on the same machine and IP address. The exported cookie from $P _ { 0 }$ is denoted as $C _ { 0 } ,$ and this setting is identified as $S _ { 0 } ,$ which is represented as $A ^ { * }$ in Figure 3.

To detect cookie restoration, we compare all cookies between $C _ { t r u e }$ and $C _ { 0 }$ , matching them based on cookie key name, value, and owner. Cookies in $C _ { 0 }$ that precisely match those in $C _ { t r u e }$ with regard to key name, value, and owner are considered restored. We collect these restored cookies into a new set called $C _ { T r u e - 0 }$

## 4.4 Detecting Fingerprinting Related Cookie Restoration

Cookie restoration may result from factors like supercookies and IP addresses. We explore whether browser fingerprinting also plays a role in cookie restoration. In setting $S _ { 1 : }$ , we maintain the same machine and IP address as in $S _ { t r u e }$ but focus on the browser finger printing aspect. We integrate Gummy Browser spoofing techniques into an extension to manipulate browser fingerprinting.

After loading the Gummy Browser extension and starting with a fresh browser profile, we visit the same website list as in $S _ { t r u e } .$ This process generates an updated browser profile, $P _ { 1 }$ , and the associated cookie, $C _ { 1 }$ . This is represented as B in Figure 3.

Distinguishing setting $S _ { 1 }$ from $S _ { t r u e } ,$ , the only variable altered is the browser fingerprinting. Therefore, any cookies in $C _ { T r u e - 0 }$ that cannot be found in $C _ { 1 }$ serve as evidence that browser fingerprinting contributes to cookie restoration. These cookies are not fully restored when browser fingerprinting is modified.

Additionally, when comparing $C _ { T r u e - 0 }$ and $C _ { 1 }$ , we may identify cookies with altered values but matching key names and owners. This observation further confirms that browser fingerprinting influences cookie restoration by demonstrating that cookie values change when fingerprinting is manipulated.

It should be noted that all settings $A 1 , A ^ { * } 1 ,$ B1 will activate simultaneously. The websites in Step 1 are listed in Appendix A.2

## 5 Experiment Setting

In this section, the objective of our experiment is to investigate the utilization of fingerprinting techniques in online advertising, particularly focusing on its impact on bid behavior and cookie restoration. The experiment is structured into several steps, each designed to simulate diferent scenarios involving fingerprinting, cookies, and IP addresses.

## 5.1 Initial Profiling and Data Collection

The first step involves the creation of an initial profile by visiting a range of websites related to "Computers". The full website list of $W _ { p }$ here is listed in Appendix A.1. During this phase, cookies are enabled, and various fingerprinting techniques are deployed to collect data for analysis. The recorded data includes fingerprinters used and data sharing activities. The generated profile is then saved for subsequent comparisons.

## 5.2 Variation in Scenarios

The second step introduces variations to the initial profile, en compassing diferent combinations of cookies, fingerprinting tech niques, and IP addresses. The scenarios examined are as follows:

a. A new profile is introduced, and bids and cookies are collected while visiting websites. This scenario provides a baseline for comparison with true fingerprints and true IP addresses (new profile, true fingerprint, true IP).

b. Profile with cookies is employed, bids and cookies are collected. This scenario explores the impact of true fingerprinting with the same IP addresses. This scenario serves as a baseline for true fingerprinting (have cookies, true fingerprint, true IP).

c. Profile with cookies is employed, with a diferent IP address and using the alternate fingerprints, while collecting bids and cookies. This scenario delves into the efects of both fake fingerprints and fake IP addresses (have cookies, fake fingerprint, true IP).

d. Profile without cookies is used to visit websites, enabling bid and cookie collection (no cookies, true fingerprint, true IP).

e. Profile without cookies is used, but with a diferent fingerprints, and bids and cookies are collected. This scenario investigates the role of diferent fingerprints with a true IP address (no cookies, fake fingerprint, true IP).

We summarize the settings in Table 1.

## 5.3 Experiment Locations

FPTrace was primarily implemented on devices situated in the United States, where we gathered bid data, monitored HTTP events, and conducted cookie restoration detection. In addition to examining regions lacking explicit privacy regulations in the United States, we also evaluated the use of browser fingerprinting in areas where privacy regulations are in place. The location selection of GDPR and CCPA experiments are explained in Appendix A.4.

## 6 Results and Evaluation

In this section, we first present the results of our experiments conducted in the United States, where privacy regulation protection was absent. These experiments were focused on data sharing and cookie restoration through browser fingerprinting, which fall outside the scope of current privacy regulations. Following this, we examine whether data sharing based on browser fingerprinting also takes place under the GDPR and CCPA privacy regulations in Appendix A.5 and A.7. The raw data we collected is listed on Onedrive [9].

## 6.1 Bid Values and HTTP Events

6.1.1 Have Cookies. We collect and analyze bids data across different settings, specifically transitioning from “have cookies, have data, true fingerprints, true IP address" to “have cookies, have data, fake fingerprints, true IP address." The sole diferentiating factor here is the presence of “true/fake fingerprints." To ensure data consistency, we conduct the experiment setting “have cookies, have data, true fingerprints, true IP address" twice to verify minimal bid data and HTTP data fluctuations. Table 2 illustrates that bid values between two instances of “True FP True IP" are quite similar, meeting our objective of running them twice. However, when comparing “True FP True IP" to “Fake FP True IP," in Table 2, there are substantial diferences in median and maximum bid values. This suggests that changes in browser fingerprinting impact bid values, implying that alterations in browser fingerprinting influence targeting and tracking in advertising.

We have also generated a CDF plot (see Figure 4a) using bid data from the two experiment settings. The distributions of CDF between diferent settings are similar when the CDF score is lower than 0.8, as all bids values are lower than 1. So we only display the distributions when the CDF scroe is larger than 0.8. In this CDF plot, the trends for two instances of “True $\mathrm { F P }$ True $\mathrm { I P " }$ are

![](images/e4224b0c963d004ba8470899b8c6f9f1b604f619bc3aa9dee3bb13dbe7b1391c.jpg)  
(a)

![](images/a2f67b40a435533051fc2d9262ef17904b1af38ecd5ca6c82c8a5f1d754c39cb.jpg)  
(b)  
Figure 4: Figure a is the CDF ofdiferentfingerprints and IPs settings in keeping cookies. Figrue b is the CDF ofdiferentfingerprints and IPs settings in removing cookies. The range ofbids value is from 0 to 5. The range ofCDF score is between 0.8 to 1. In Figure a, We can observe that the red curve is much diferentfrom the other two curves which are closer to each other, thus showing that fingerprinting is being used for tracking. In Figure b We can observe that the red curve is much diferent from the other two curves which are closer to each other, thus showing thatfingerprinting is being usedfor tracking.

Table 2: The bid value in diferent fingerprints and IPs settings. Avg represents the average ofall bid value. Median represents the median bid value. Min represents the minimum bid value. Max represents the maximum bid value. We can observe that the first row values are diferent from the other two rows, which are similar to each other, thus showing that the change in FP creates a more marked impact on the bid values indicating thatfingeprinting is being usedfor tracking.

<table><tr><td></td><td>Avg</td><td>Std</td><td>Median</td><td>Min</td><td>Max</td></tr><tr><td>Fake FP True IP</td><td>0.60</td><td>1.14</td><td>0.19</td><td>0.00</td><td>10.02</td></tr><tr><td>True FP True IP</td><td>0.51</td><td>0.86</td><td>0.25</td><td>0.00</td><td>5.45</td></tr><tr><td>True FP True IP 2</td><td>0.46</td><td>0.93</td><td>0.23</td><td>0.00</td><td>5.52</td></tr></table>

also similar, signifying that bid data remains stable under the same browser fingerprint. However, the introduction of fake fingerprints alters the trend of bid data. This indicates a significant diference in the distribution of bids between the two settings. The CDF plot provides evidence that changes in browser fingerprinting afect targeting and tracking in advertising.

Furthermore, we calculated the number of HTTP chains, sync ing events, and total HTTP records using HTTP data from the two settings. The results are outlined in Table 3. It is evident that the number of total HTTP chains in two instances of “True FP True IP" is similar and exceeds 36,000. However, changing the browser fingerprint reduces this number to 6,345, a substantial drop. This reduction indicates fewer HTTP chains can be established, imply ing a decrease in redirects and a reduced ability for websites to recognize the browser profile. A similar pattern emerges in syncing events: the number of syncing events in “Fake FP True IP" is 50% less than in “True FP True IP," signifying a 50% reduction in data sharing. The total number of HTTP records in “Fake FP True IP" is nearly 65% less than in “True FP True IP." The decrease in HTTP records also implies reduced recognition on the internet.

```txt
Takeaway [Have Cookies]: (1) Bids trend and range are changed after changing the browser fingerprinting. (2) HTTP chains, syncing events and total records drop after changing the browser fingerprinting.
```

6.1.2 No Cookies. We gather and scrutinize bid data across vari ous scenarios, particularly transitioning from a state characterized by “no cookies, have data, true fingerprints, true IP address" to a state with “no cookies, have data, true fingerprints, true IP address". To ensure the consistency of the data, we repeat the experiment under the setting “have cookies, have data, true fingerprints, true IP address" to confirm minimal variations in bid data and HTTP data. In the context of “true fingerprints", we introduce one fabricated fingerprint, while “fake fingerprints" includes another counterfeit fingerprint. Table 4 provides an overview of bid values across these three diferent configurations. When we keep the fingerprints consistent and eliminate cookies, the average and median bid values experience marginal increases, but the maximum bid value rises significantly. Following the alteration of fingerprints, both the average and maximum bid values increase, while the median value experiences a notable decrease. This suggests that changes in browser fingerprinting have an impact on bid values, underscoring their influence on targeting and tracking in advertising.

Table 3: The number of events and data through HTTP data. Chains represents the number ofchains we built using collected HTTP data. Syncing represents the number of chains containing the data sharing. Records represents the total number ofHTTP records collected in this settings. We can observe that the first row values are diferent from the other two rows, which are similar to each other, thus showing that the change in FP creates a more marked impact on the bid values indicating that fingeprinting is being used for tracking.

<table><tr><td></td><td>Chains</td><td>Syncing</td><td>Records</td></tr><tr><td>Fake FP True IP</td><td>6345</td><td>421</td><td>109802</td></tr><tr><td>True FP True IP</td><td>36446</td><td>888</td><td>313094</td></tr><tr><td>True FP True IP 2</td><td>37929</td><td>895</td><td>318208</td></tr></table>

Table 4: The bid value in diferent fingerprints and IPs settings. Avg represents the average of all bid value. Median represents the median bid value. Min represents the minimum bid value. Max represents the maximum bid value. Setting “True FP True IP 2” do keep the cookies. Other two settings do not keep the cookies.

<table><tr><td></td><td>Avg</td><td>Std</td><td>Median</td><td>Min</td><td>Max</td></tr><tr><td>Fake FP True IP</td><td>0.42</td><td>0.89</td><td>0.13</td><td>0.00</td><td>5.92</td></tr><tr><td>True FP True IP</td><td>0.38</td><td>0.54</td><td>0.19</td><td>0.00</td><td>5.80</td></tr><tr><td>True FP True IP 2</td><td>0.35</td><td>0.41</td><td>0.17</td><td>0.00</td><td>2.13</td></tr></table>

We have also generated a CDF plot (see Figure 4b) using bid data from the two experimental configurations. The distributions of CDF between diferent settings are similar when the CDF score is lower than 0.8, as all bids values are lower than 1. So we only display the distributions when the CDF scroe is larger than 0.8. In this CDF plot, the patterns for two instances of "True FP True IP" are notably similar, indicating that bid data remains stable when the same browser fingerprint is used. However, the introduction of fake fingerprints disrupts the trend of bid data, signifying a substantial diference in bid distribution between the two settings. The CDF plot furnishes evidence that variations in browser fingerprinting influence targeting and tracking in advertising.

Furthermore, we computed the number ofHTTP chains, synchronization events, and total HTTP records using HTTP data from the two configurations. The outcomes are summarized in Table 5. It is apparent that the total number of HTTP chains remains comparable across all three settings. Upon the removal of cookies, this number decreased by approximately 13 percent, and further dropped by 2 percent when cookies were changed. The number of synchronization events exhibited consistency across the three settings, while the total count of HTTP records continued to decrease after cookies were removed and fingerprints were altered. The decrease in HTTP records also suggests reduced online recognition.

Table 5: The number of events and data through HTTP data. Chains represents the number ofchains we built using collected HTTP data. Syncing represents the number of chains containing the data sharing. Records represents the total number ofHTTP records collected in this settings. CR represents the setting of Cookie Removed. All data are from settings including removing cookies.

<table><tr><td></td><td>Chains</td><td>Syncing</td><td>Records</td></tr><tr><td>Fake FP True IP (CR)</td><td>9606</td><td>632</td><td>119673</td></tr><tr><td>True FP True IP (CR)</td><td>9796</td><td>624</td><td>124543</td></tr><tr><td>True FP True IP 2</td><td>11242</td><td>649</td><td>128781</td></tr></table>

Takeaway [No Cookies]:

(1) Bids trend and range are changed after removing cookies and changing the browser fingerprinting.

(2) HTTP chains, and total records drop after removing cookies and changing the browser fingerprinting.

Based on our analysis of bid values and HTTP events, we can draw the conclusion that browser fingerprinting plays a significant role in targeting and tracking within the realm of advertising.

## 6.2 Cookie Restoration

After the cookie data comparison, we totally detected 90 cookie key and host pairs. We documented 378 instances of cookie restoration related to fingerprinting across 90 unique combinations of cookie keys and host pairs across all settings. Subsequently, we conducted a comprehensive manual inspection of all 90 cookie key and host pair combinations. In light of our thorough experiments, we can not definitively assert that browser fingerprinting is employed to restore cookies. The full details are listed in Appendix A.6.

## 7 Discussion and Limitations

Our experiment was conducted using IP addresses from two loca tions in the United States, both of which are located in the United States and are not subject to privacy regulations such as GDPR [1] or CCPA [2]. In regions protected by such regulations, trackers like cookies are prohibited from tracking users once they opt out. However, our experiment has revealed that advertisers may em ploy browser fingerprinting to track users without providing any notification. It remains uncertain whether advertisers can continue using browser fingerprinting to track users, as there is currently no established framework for auditing advertisers in this context. It’s important to note that our experiment cannot be utilized to assess advertisers’ behavior within the constraints of privacy regulations.

Another limitation of our study is that all experiments were conducted on the Linux platform. We cannot determine whether users of Windows devices, MacOS devices, or mobile devices can still be tracked by advertisers using browser fingerprinting tech niques. While some of our fake fingerprint data were obtained from Windows devices, MacOS devices, or mobile devices, which we used to emulate our experimental device browsers, it would be valuable to incorporate real Windows devices, MacOS devices, or mobile devices in the “True Fingerprints" settings to gain a more comprehensive understanding.

Additionally, there is uncertainty regarding whether websites visited by FPTrace can accurately distinguish between visits from a crawler and those from real users. Despite our eforts, such as altering JS API values and simulating human behaviors, we cannot be entirely certain that there are no undisclosed techniques for detecting bot visits. If FPTrace’s visits are identified as originating from a bot, the accuracy of our results may be compromised.

Compared to the work of Liu et al.[34], there are notable diferences in our study in both experimental design and research objectives. While our work focuses on exploring various fingerprinting settings and assessing whether diferent privacy regulations can constrain fingerprinting techniques, Liu et al.[34] did not involve any specific fingerprinting configurations. Instead, their research aimed to evaluate whether CMPs, websites, or advertisers comply with users’ consent choices.

## 8 Related Work

Previous research has examined the connection between online tracking and ad targeting. Wills et al.[44] explored Google and Facebook’s ad systems, identifying various ad types. Google sometimes showed non-contextual ads related to sensitive topics, even without relevant user activity. On Facebook, external browsing had no clear link to ads, but using the “Like” feature on third-party content influenced ad recommendations. Zeng et al.[47] studied the impact of user attributes, demographics, and contextual factors on ad targeting and bid values. Using data from 286 participants across 10 websites, they found targeting was primarily shaped by the website, retargeting methods, and user behavior, with demographics playing a minor role. Variations in bid values were mostly linked to the website and user actions, highlighting the significance of contextual targeting. Cassel et al.[22] analyzed web tracking across devices, noting fewer tracking requests on mobile. Privacy-focused browsers reduced tracking but showed susceptibility to fingerprinting, without delving into its role in ads. Fouad et al.[27] investigated cookie restoration using VPNs, which might introduce latency. Our approach, using real IPs and manual inspections, revealed that factors like time and website data could lead to restoration resembling fingerprinting.

## 9 Conclusion

In this study, we address a gap in research and regulatory practices by investigating browser fingerprinting’s role in ad tracking. We introduce “FPTrace”, a framework for detecting fingerprinting usage, especially when changes in fingerprints disrupt ad target ing. FPTrace is evaluated in web environments where user data is routinely collected for ads. Our method involves A/B experiments, data leakage analysis, fingerprint manipulation, and ad bidding analysis to study how altered fingerprints afect cookie restoration, hypothesizing that prior user knowledge influences bid changes.

Key contributions include the FPTrace framework, integrated with OpenWPM, which simulates user interactions, collects bid data, and records HTTP data. Our findings show browser fingerprinting significantly impacts ad tracking, with noticeable diferences in bid values and a reduction in HTTP records when fingerprints change. While fingerprints and cookies show some connection, evidence of direct involvement in cookie restoration remains inconclusive.

## Acknowledgments

We would like to thank anonymous reviewers for their helpful comments and feedback. This work was supported in part by National Science Foundation (NSF) under grants CCF-2317185, OAC-2139358, CNS- 2201465, and CNS-2154507.

## References

[1] 2016. Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation). https://eur-lex.europa.eu/eli/re g/2016/679/oj/eng.

[2] 2018. California Consumer Privacy Act. https://leginfo.legislature.ca.gov/faces /codes\_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5.

[3] 2020. Fraud detection API demo. https://fingerprintjs.com/demo.

[4] 2023. Browser Fingerprinting: A Complete Guide. https://incogniton.com/bro wser-fingerprinting-complete-guide.

[5] 2023. Client-side vs. Server-side Header Bidding: What to Choose? https://www.adpushup.com/blog/client-side-header-bidding-vs-server-sideheader-bidding/.

[6] 2023. Cover Your Track. https://coveryourtracks.eff.org/.

[7] 2023. DataDome - Bot & Online Fraud Protection Solution. https://datadome.co/.

[8] 2023. DDoS Services: Cloud Security Products and Solutions | Radware. https: //www.radware.com/.

[9] 2023. The First Early Evidence of the Use of Browser Fingerprinting for Online Tracking raw data. https://tamucs-my.sharepoint.com/:f:/g/personal/lzr\_tamu \_edu/EtA94fEfURxHsH6Qixvrvn4BnLJWHzMoM\_EHeF4Vx3n78A?e=xhavnq.

[10] 2023. Header Bidding. https://admanager.google.com/home/resources/featurebrief-open-bidding/.

[11] 2023. How to use ModHeader in Selenium WebDriver. https://modheader.com/ docs/advanced/selenium-webdriver.

[12] 2023. ModHeader. https://chrome.google.com/webstore/detail/modheader/idgp nmonknjnojddfkpgkljpfnnfcklj?hl=en.

[13] 2023. My browser fingerprint. https://amiunique.org/fp.

[14] 2023. Network Advertising Initiative (NAI) opt-out controls. https://optout.net workadvertising.org/?c=1.

[15] 2023. Prebid. https://prebid.org/.

[16] 2023. Protection From Automated Attacks, Bots and Fraud | HUMAN Security. https://www.humansecurity.com/.

[17] 2023. Selenium automates browsers. That’s it! https://www.selenium.dev/.

[18] 2023. Web Almanac: Part II Chapter 10 Privacy: Consent Management Platforms. https://almanac.httparchive.org/en/2021/privacy.

[19] Gunes Acar, Marc Juarez, Nick Nikiforakis, Claudia Diaz, Seda Gürses, Frank Piessens, and Bart Preneel. 2013. FPDetective: dusting the web for fingerprinters. In Proceedings ofthe 2013 ACM SIGSAC conference on Computer & communications security. 1129–1140.

[20] Károly Boda, Ádám Máté Földes, Gábor György Gulyás, and Sándor Imre. 2012. User tracking on the web via cross-browser fingerprinting. In Information Security Technology for Applications: 16th Nordic Conference on Secure IT Systems, NordSec 2011, Tallinn, Estonia, October 26-28, 2011, Revised Selected Papers 16. Springer, 31–46.

[21] Yinzhi Cao, Song Li, and Erik Wijmans. 2017. (Cross-) browser fingerprinting via OS and hardware level features. In Proceedings 2017 Network and Distributed System Security Symposium. Internet Society.

[22] Darion Cassel, Su-Chin Lin, Alessio Buraggina, William Wang, Andrew Zhang, Lujo Bauer, Hsu-Chun Hsiao, Limin Jia, and Timothy Libert. 2021. Omnicrawl: Comprehensive measurement of web tracking with real desktop and mobile browsers. Proceedings on Privacy Enhancing Technologies 2022, 1 (2021).

[23] John Cook, Rishab Nithyanand, and Zubair Shafiq. 2020. Inferring Tracker-Advertiser Relationships in the Online Advertising Ecosystem using Header Bidding. In Privacy Enhancing Technologies Symposium (PETS).

[24] Peter Eckersley. 2010. How unique is your web browser?. In International Symposium on Privacy Enhancing Technologies Symposium.

[25] Steven Englehardt and Arvind Narayanan. 2016. Online Tracking: A 1-million-site Measurement and Analysis. In ACM Conference on Computer and Communications Security (CCS).

[26] David Fifield and Serge Egelman. 2015. Fingerprinting web users through font metrics. In International Conference on Financial Cryptography and Data Security.

[27] Imane Fouad, Cristiana Santos, Arnaud Legout, and Nataliia Bielova. 2022. My Cookie is a phoenix: detection, measurement, and lawfulness of cookie respawn ing with browser fingerprinting. In PETS 2022-22nd Privacy Enhancing Technologies Symposium.

[28] Umar Iqbal, Steven Englehardt, and Zubair Shafiq. 2021. Fingerprinting the fingerprinters: Learning to detect browser fingerprinting behaviors. In 2021 IEEE Symposium on Security and Privacy (SP). IEEE, 1143–1161.

[29] Pierre Laperdrix, Gildas Avoine, Benoit Baudry, and Nick Nikiforakis. 2019. Morellian analysis for browsers: Making web authentication stronger with canvas fingerprinting. In International Conference on Detection ofIntrusions and Malware, and Vulnerability Assessment. Springer, 43–66.

[30] Pierre Laperdrix, Nataliia Bielova, Benoit Baudry, and Gildas Avoine. 2020. Browser Fingerprinting: A Survey. ACM Trans. Web 14, 2, Article 8 (apr 2020), 33 pages.

[31] Pierre Laperdrix, Walter Rudametkin, and Benoit Baudry. 2016. Beauty and the beast: Diverting modern web browsers to build unique browser fingerprints. In 2016 IEEE Symposium on Security and Privacy (SP). IEEE, 878–894

[32] Ada Lerner, Anna Kornfeld Simpson, Tadayoshi Kohno, and Franziska Roesner. 2016. Internet Jones and the Raiders of the Lost Trackers: An Archaeological Study of Web Tracking from 1996 to 2016. In 25th USENIX Security Symposium (USENIX Security 16). USENIX Association, Austin, TX. https://www.usenix.org /conference/usenixsecurity16/technical-sessions/presentation/lerner

[33] Xu Lin, Panagiotis Ilia, Saumya Solanki, and Jason Polakis. 2022. Phish in Sheep’s Clothing: Exploring the Authentication Pitfalls of Browser Fingerprinting. In 31st USENIX Security Symposium (USENIX Security 22). 1651–1668.

[34] Zengrui Liu, Umar Iqbal, and Nitesh Saxena. 2024. Opted Out, Yet Tracked: Are Regulations Enough to Protect Your Privacy? Proceedings on Privacy Enhancing Technologies (2024).

[35] Zengrui Liu, Prakash Shrestha, and Nitesh Saxena. 2022. Gummy browsers: targeted browser spoofing against state-of-the-art fingerprinting techniques. In International Conference on Applied Cryptography and Network Security. Springer, 147–169.

[36] Keaton Mowery and Hovav Shacham. 2012. Pixel perfect: Fingerprinting canvas in HTML5. Proceedings ofW2SP 2012 (2012).

[37] Martin Mulazzani, Philipp Reschl, Markus Huber, Manuel Leithner, Sebastian Schrittwieser, Edgar Weippl, and FC Wien. 2013. Fast and reliable browser identification with javascript engine fingerprinting. In Web 2.0 Workshop on Security and Privacy (W2SP), Vol. 5. Citeseer, 4.

[38] Gabi Nakibly, Gilad Shelef, and Shiran Yudilevich. 2015. Hardware fingerprinting using HTML5. arXiv preprint arXiv:1503.01408 (2015).

[39] Nick Nikiforakis, Alexandros Kapravelos, Wouter Joosen, Christopher Kruegel, Frank Piessens, and Giovanni Vigna. 2013. Cookieless monster: Exploring the ecosystem of web-based device fingerprinting. In 2013 IEEE Symposium on Security and Privacy. IEEE, 541–555.

[40] Lukasz Olejnik, Minh-Dung Tran, and Claude Castelluccia. 2014. Selling Of Privacy at Auction. In Network and Distributed System Security Symposium (NDSS).

[41] Alexander Sjösten, Daniel Hedin, and Andrei Sabelfeld. 2021. Essentialfp: Exposing the essence of browser fingerprinting. In 2021 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW). IEEE, 32–48

[42] Spirals-Team. 2020. Spirals-Team/FPStalker. https://github.com/Spirals-Team/FPStalker.

[43] Antoine Vastel, Pierre Laperdrix, Walter Rudametkin, and Romain Rouvoy. 2018. {Fp-Scanner}: The privacy implications of browser fingerprint inconsistencies. In 27th USENIX Security Symposium (USENIX Security 18). 135–150

[44] Craig E Wills and Can Tatar. 2012. Understanding what they do with what they know. In Proceedings of the 2012 ACM Workshop on Privacy in the Electronic Society. 13–18.

[45] Shujiang Wu, Pengfei Sun, Yao Zhao, and Yinzhi Cao. 2023. Him of many faces: Characterizing billion-scale adversarial and benign browser fingerprints on commercial websites. In 30th Annual Network and Distributed System Security Symposium, NDSS.

[46] Ting-Fang Yen, Yinglian Xie, Fang Yu, Roger Peng Yu, and Martin Abadi. 2012. Host Fingerprinting and Tracking on the Web: Privacy and Security Implications.. In NDSS, Vol. 62. 66.

[47] Eric Zeng, Rachel McAmis, Tadayoshi Kohno, and Franziska Roesner. 2022. What factors afect targeting and bids in online advertising? a field measurement study. In Proceedings ofthe 22nd ACM Internet Measurement Conference. 210–229.

## A Appendix

## A.1 Training Websites

(1) https://www.bestbuy.com/site/electronics/computers-pcs/ abcat0500000.c?id=abcat0500000

(2) https://www.newegg.com/Computer-Systems/Store/ID-3

(3) https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&s t=best+buy+computers+for+sale

(4) https://www.pcmag.com/picks/the-best-desktop-computer s

(5) https://www.consumerreports.org/cro/computers/buyingguide/index.htm

Zengrui Liu, Jimmy Dani, Yinzhi Cao, Shujiang Wu, and Nitesh Saxena

(6) https://www.walmart.com/cp/computers/3951

(7) https://www.amazon.com/Computers-Tablets/b?ie=UTF8&n ode=13896617011

(8) http://www.newegg.com/

(9) https://www.dell.com/en-us

(10) https://www.hp.com/us-en/shop/cat/desktops

(11) https://www.adorama.com/l/Computers

(12) https://edu.gcfglobal.org/en/computerbasics/what-is-a-co mputer/1/

(13) https://www.tomsguide.com/best-picks/best-computers

(14) https://www.costco.com/computers.html

(15) https://www.microsof t.com/en-us/store/b/pc

(16) https://www.britannica.com/technology/computer

(17) https://www.cyberpowerpc.com/page/Intel/11th-Gen-Desk tops/

(18) https://www.backmarket.com/refurbished-pc-desktop-co mputer.html

(19) https://www.bhphotovideo.com/c/browse/Computers-Solu tions/ci/9581

(20) https://www.microcenter.com/

(21) https://www.target.com/c/computers-office-electronics/-/N-5xtfc

(22) https://www.officedepot.com/cm/tech/shop-pcs

(23) https://www.tigerdirect.com/

(24) https://www.staples.com/Laptops-Computers/cat\_SC3

(25) https://www.lenovo.com/us/en/

(26) https://www.cdw.com/content/cdw/en/products/computers. html

(27) https://www.energystar.gov/products/computers

(28) https://www.xidax.com/xidaxsale

(29) https://buildredux.com

(30) https://www.corsair.com

(31) https://www.magicmicro.com

(32) https://www.thebudgetpcbuilder.com/

(33) https://www.ebay.com/b/Computers-Tablets-Network-Ha rdware/58058/bn\_1865247

(34) https://computersfortheblind.org/

(35) https://www.nytimes.com/wirecutter/electronics/compute rs/

(36) https://www.samsung.com/us/computing/

(37) https://www.lg.com/us/computers

(38) https://www.apple.com/

(39) https://www.sciencedirect.com/journal/computers-enviro nment-and-urban-systems

(40) https://www.ibuypower.com/

A.2 Testing Websites

(1) https://tribunnews.com

(2) https://grid.id

(3) https://nytimes.com

(4) https://ettoday.net

(5) https://kompas.com

(6) https://indiatimes.com

(7) https://globo.com

(8) https://liputan6.com

(9) https://uol.com.br

(10) https://speedtest.net

(11) https://alwafd.news

(12) https://theguardian.com

(13) https://espn.com

(14) https://cnet.com

(15) https://brilio.net

The First Early Evidence of the Use of Browser Fingerprinting for Online Tracking

(16) https://businessinsider.com

(17) https://foxnews.com

(18) https://breitbart.com

(19) https://metropoles.com

(20) https://ladbible.com

(21) https://investopedia.com

(22) https://realtor.com

(23) https://nypost.com

(24) https://sportbible.com

(25) https://hurriyet.com.tr

(26) https://goo.ne.jp

(27) https://softonic.com

## A.3 GDPR and CCPA Configuration

In GDPR and CCPA experiments, we set 6 diferent settings on each CMP and location combination. The number of each setting is described as following:

(0) New profile, True fingerprint.

(1) Trained profile, True fingerprint, Have Cookies. (Base Line)

(2) Trained profile, Fake fingerprint, Have Cookies.

(3) Trained profile, True fingerprint, Have Cookies. (Same set ting as 1)

(4) Trained profile, Fake fingerprint, No Cookies.

(5) Trained profile, True fingerprint, No Cookies.

The complete workflow of GDPR and CCPA experiments is listed in Figure 5. Four CMPs Cookiebot, Quantcast, Onetrust, and Didomi CMPs are employed in our experiments, along with the central opt out platform NAI. True or fake fingerprints are set in step C in Figure 5.

In our experiments, “Opt out” refers to scenarios where the user declines to provide consent to the website, while “Opt in” denotes instances where the user grants consent. All interactions with these diferent CMPs are conducted automatically.

## A.4 Experiment Locations

Privacy regulations like the General Data Protection Regulation (GDPR) [1] and the California Consumer Privacy Act (CCPA) [2] are designed to safeguard user personal information. Under GDPR, cus tomers have assurance against privacy breaches until they consent on websites. For CCPA protection, customers must actively refuse consent on websites to avoid privacy breaches. In our experimental setup, we initially evaluate data sharing related to fingerprinting and cookie restoration using local IP addresses in locations within the United States, where privacy regulation protection was absent.

![](images/c4a3ebf69f0c1a6fef3829c54c5d28ed714a9209a5433cb392d63ecc04fc72ab.jpg)  
Figure 5: High level overview ofGDPR/CCPA experiment. Step A represents the training persona, with the original fingerprint. Step B involves Opt Out or Opt In actions on websites with ads, utilizing CMPs, and employing Prebid.js, or on the central Opt Out website NAI. Step C involves the collection of HTTP data. Step D represents the data analysis.

Subsequently, we implement FPTrace on AWS servers located in Frankfurt, Germany, and California, USA. Frankfurt-based visits fall under GDPR protection, while those from California are under CCPA. The aim of selecting these varied regions is to discern the impact of browser fingerprinting in environments with and without privacy regulation protection.

For visitors accessing websites from Europe or California, USA, the sites are expected to present a consent panel, allowing them to either agree or refuse consent. CMPs are third-party services that facilitate this consent process for users. There is a variety of CMP services available. As identified by Liu et al.[34], four prominent CMPs - Cookiebot, Quantcast, Onetrust, and Didomi - are among the most widely used and can be considered for use in this context. FPTrace can automatically handle the opt-out and opt-in. To ensure compliance with Didomi, we first verify the existence of the consent dialog using Didomi.notice.isVisible. We then employ Didomi.setUserDisagreeToAll to opt out and proceed to conceal the consent dialog by adjusting the display attributes of its markup to ‘none’. Similarly, for OneTrust, we confirm the presence of the consent dialog via window.OneTrust, executing window.OneTrust.RejectAll to opt out and subsequently conceal the dialog. In the case of CookieBot, we validate the presence of the consent dialog through window.Cookiebot, navigating the DOM to locate the opt-out button with the ID CybotCookiebotDialogBody-ButtonDecline and activating it. Regarding Quantcast, we search the DOM for the consent dialog using the qc-cmp2-summary-buttons class name, clicking the button labeled ‘Reject’ or similar. If the rejection option is not initially visible, we expand the dialog by selecting the ’more options’ button and then proceed to click ‘Reject All’. Additionally, we assess the efectiveness of the central opt-out service Network Advertising Initiative (NAI) [14], which enables users to refuse consent through a single visit to its website. Consequently, other websites should comply by not utilizing the users’ consent if this service is used.

Table 6: The number ofevents and data through HTTP data. The CMP is: Onetrust and the Privacy Regulation is: CCPA. Total HTTP Records represents the total number ofHTTP records collected in this settings. Total HTTP Chains represents the number ofchains we built using collected HTTP data. Syncing Events represents the number of chains containing the data sharing. All data are from settings including removing cookies. We can analyze the data from both setting 1 and setting 2. There are minimal diferences observed in Opt In setting. A significant diference was noticed in the Opt Out setting when comparing settings 2 and 1, suggesting that fingerprint changes may afect the tracking.

<table><tr><td colspan="7">Onetrust</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>1549</td><td>302</td><td>50928</td><td>1178</td><td>334</td><td>43107</td></tr><tr><td>1</td><td>724</td><td>199</td><td>38720</td><td>754</td><td>238</td><td>39001</td></tr><tr><td>2</td><td>2216</td><td>395</td><td>46595</td><td>1593</td><td>401</td><td>44221</td></tr><tr><td>3</td><td>1588</td><td>407</td><td>46257</td><td>1618</td><td>381</td><td>49725</td></tr><tr><td>4</td><td>1204</td><td>368</td><td>45948</td><td>1657</td><td>449</td><td>45742</td></tr><tr><td>5</td><td>1084</td><td>227</td><td>42639</td><td>1663</td><td>417</td><td>50911</td></tr></table>

Table 7: The number ofevents and data through HTTP data. The CMP is: Onetrust and the Privacy Regulation is: GDPR. Total HTTP Records represents the total number of HTTP records collected in this settings. Total HTTP Chains represents the number of chains we built using collected HTTP data. Syncing Events represents the number of chains containing the data sharing. All data are from settings including removing cookies. We can analyze the data from both setting 1 and setting 2. There are minimal diferences observed in Opt In setting. A significant diference ofsyncing events was noticed in the Opt Out setting when comparing settings 2 and 1, suggesting thatfingerprint changes may afec the tracking.

<table><tr><td colspan="7">Onetrust</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>400</td><td>10</td><td>38194</td><td>423</td><td>33</td><td>38587</td></tr><tr><td>1</td><td>400</td><td>21</td><td>37350</td><td>505</td><td>36</td><td>44067</td></tr><tr><td>2</td><td>455</td><td>42</td><td>38636</td><td>485</td><td>61</td><td>38783</td></tr><tr><td>3</td><td>474</td><td>29</td><td>39754</td><td>546</td><td>41</td><td>42426</td></tr><tr><td>4</td><td>708</td><td>99</td><td>42782</td><td>482</td><td>47</td><td>39095</td></tr><tr><td>5</td><td>516</td><td>34</td><td>41560</td><td>395</td><td>19</td><td>38807</td></tr></table>

## A.5 Browser Fingerprinting Data Sharing under Privacy Regulations

Tables of full results from CMP Cookiebot, Didomi and Quantcast, and NAI are listed in Appendix A.7.

Under GDPR regulations, Cookiebot showed a significant in crease in the number of HTTP Chains, Syncing Events, and HTTP records when cookies were removed, observed in both Opt Out and Opt In settings. However, using a fake fingerprint did not result in notable changes in either setting. Full details are listed in Appendix A.7 Table 9.

With Didomi, also under GDPR, the various settings, including Opt Out versus Opt In and True/Fake fingerprint or Have/No Cook ies scenarios, did not exhibit substantial diferences. Full details are listed in Appendix A.7 Table 11.

In the case of Onetrust, under GDPR conditions, an increase in Syncing Events was observed when the system utilized fake finger prints. This rise was particularly notable in scenarios combining Fake Fingerprint and No Cookies in the Opt Out setting, suggesting that browser fingerprinting might be used for data syncing even after users deny consent on websites using Onetrust. Full details are listed in Table 7.

For Quantcast, regardless of Opt Out or Opt In settings under GDPR, the application of Fake Fingerprint led to a more pronounced increase in syncing events than in HTTP chains. This suggests that browser fingerprinting might be employed for syncing data regardless of whether the user consents or denies consent on websites using Quantcast. Full details are listed in Appendix A.7 Table 13.

Lastly, in the context of NAI under GDPR, a pattern similar to Quantcast was observed. The number of syncing events and HTTP chains significantly increased when the fingerprints were altered, indicating that browser fingerprinting might be used for data syncing irrespective of the user’s decision to give or reject consent on the NAI website. Full details are listed in Appendix A.7 Table 15.

## Takeaway [Browser Fingerprinting in GDPR]:

(1) There is no conclusive evidence to suggest that Cookiebot and Didomi participate in data sharing through browser fingerprinting for user identification in both Opt Out and Opt In settings. Websites utilizing Onetrust might not be involved in data sharing activities that use browser fingerprinting to identify users in Opt In setting.

(2) It appears that websites utilizing Onetrust, Quantcast, and NAI might be involved in data sharing activities that use browser fingerprinting to identify users in Opt Out setting. Quantcast and NAI might be involved in data sharing activities that use browser fingerprinting to identify users in Opt In setting.

Under the CCPA regulation, Cookiebot’s diverse settings, such as Opt Out vs Opt In and True/Fake fingerprint or Have/No Cookies scenarios, showed no significant diferences. Full details are listed in Appendix A.7 Table 8.

Likewise, under CCPA regulation, Didomi’s settings, including Opt Out vs Opt In and True/Fake fingerprint or Have/No Cookies scenarios, displayed no notable diferences. Full details are listed in Table Appendix A.7 10.

Under CCPA regulations, with Onetrust, a notable disparity was observed in the Opt Out setting between settings 2 and 1, as well as between 2 and 3. This suggests possible use of browser finger printing in data synchronization. Full details are listed in Table 6.

In the case of Quantcast, under CCPA regulation, the various settings including Opt Out vs Opt In and True/Fake fingerprint or Have/No Cookies scenarios, also showed negligible diferences. Full details are listed in Appendix A.7 Table 12.

Lastly, under CCPA regulation with NAI, in the Opt Out setting, there was a significant diference between setting 2 and both set tings 1 and 3, indicating a potential use of browser fingerprinting for data synchronization. Full details are listed in Appendix A.7 Table 14.

Takeaway [Browser Fingerprinting in CCPA]:

(1) There is no conclusive evidence to suggest that Cookiebot, Didomi and Quantcast participate in data sharing through browser fingerprinting for user identification in both Opt Out and Opt In settings. Websites utilizing Onetrust, and NAI might not be involved in data sharing activities that use browser fingerprinting to identify users in Opt In setting.

(2) It appears that websites utilizing Onetrust, and NAI might be involved in data sharing activities that use browser fingerprinting to identify users in Opt Out setting.

## A.6 Cookie Restoration Results

After the cookie data comparison, we totally detected 90 cookie key and host pairs, for example: key “acc\_segment” and host “sgqcvfjvr-.onet.pl”. Fingerprinting related cookie restoration behaviors are found under all settings: All changes, Languages, OS, appVersion, UserAgent, Vendor, CookieEnabled, doNotTrack, Language, Plugin, Canvas. In UserAgent, Languages and Language settings, we not only change the value JS API “Navigator”, but also change the value in HTTP header. The following is the example of cookie value changed after fingerprints are changed.

domain : google .it key: OTZ value : 1. 7151858 \_76\_80\_104160\_76\_446820 (UA: chrome ) 2. 7151859 \_76\_80\_104160\_76\_446820 (UA: firefox )

In total, we documented 378 instances of cookie restoration related to fingerprinting across 90 unique combinations of cookie keys and host pairs across all settings. Subsequently, we conducted a comprehensive manual inspection of all 90 cookie key and host pair combinations. However, the results of our examination do not provide substantial support for the assertion that these cookie restorations are linked to fingerprinting.

Throughout our manual inspection, we observed that some values did indeed change when we altered the browser fingerprint, while others exhibited variations correlating with the passage of time. Additionally, certain values appeared to be random, deriving from an unidentified source. For identical cookie key and host pairs, we encountered instances where the same value persisted during two inspections with diferent fingerprints, as well as situations where the same value occurred during two inspections with the same fingerprints. Furthermore, some values incorporated fingerprinting feature values, suggesting that alterations in browser fingerprints influenced the cookie value. Nonetheless, these changes cannot be unequivocally attributed to browser fingerprinting restoration.

Takeaway [Cookie Restoration]:

(1) During the data collection process for automation, we observed that certain cookies are reinstated when fingerprints remain consistent. However, when these fingerprints are altered, the values of these cookies either change or they vanish.

(2) Upon manual examination, the restoration of these cookies was determined not to be related to fingerprinting.

In light of our thorough manual inspection, we cannot definitively assert that browser fingerprinting is employed to restore cookies.

## A.7 Analysis of HTTP data under GDPR and CCPA

Within this section, we provide information in additional tables for the analysis of HTTP data under the protection of GDPR or CCPA.

Table 8: The number ofevents and data through HTTP data. The CMP is: Cookiebot and the Privacy Regulation is: CCPA. Total HTTP Records represents the total number ofHTTP records collected in this settings. Total HTTP Chains represents the number ofchains we built using collected HTTP data. Syncing Events represents the number ofchains containing the data sharing. All data are from settings including removing cookies. We can analyze the data from both setting 1 and setting 2. There are minimal diferences observed in both Opt Out and Opt In settings.

<table><tr><td colspan="7">Cookiebot</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>248</td><td>61</td><td>7934</td><td>315</td><td>104</td><td>8863</td></tr><tr><td>1</td><td>392</td><td>175</td><td>9197</td><td>459</td><td>125</td><td>9568</td></tr><tr><td>2</td><td>407</td><td>149</td><td>9249</td><td>509</td><td>154</td><td>9251</td></tr><tr><td>3</td><td>363</td><td>120</td><td>8981</td><td>344</td><td>94</td><td>8365</td></tr><tr><td>4</td><td>238</td><td>55</td><td>7727</td><td>505</td><td>141</td><td>9175</td></tr><tr><td>5</td><td>241</td><td>57</td><td>7664</td><td>292</td><td>131</td><td>7959</td></tr></table>

Table 9: The number ofevents and data through HTTP data. The CMP is: Cookiebot and the Privacy Regulation is: GDPR. Total HTTP Records represents the total number ofHTTP records collected in this settings. Total HTTP Chains represents the number ofchains we built using collected HTTP data. Syncing Events represents the number ofchains containing the data sharing. All data are from settings including removing cookies. We can analyze the data from both setting 1 and setting 2. There are minimal diferences observed in both Opt Out and Opt In settings

<table><tr><td colspan="7">Cookiebot</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>133</td><td>5</td><td>7515</td><td>128</td><td>3</td><td>7068</td></tr><tr><td>1</td><td>118</td><td>3</td><td>7080</td><td>118</td><td>4</td><td>7226</td></tr><tr><td>2</td><td>123</td><td>4</td><td>7537</td><td>119</td><td>3</td><td>7116</td></tr><tr><td>3</td><td>123</td><td>5</td><td>7512</td><td>118</td><td>5</td><td>7371</td></tr><tr><td>4</td><td>253</td><td>14</td><td>15836</td><td>223</td><td>6</td><td>14367</td></tr><tr><td>5</td><td>228</td><td>8</td><td>14423</td><td>229</td><td>6</td><td>15352</td></tr></table>

Table 10: The number ofevents and data through HTTP data. The CMP is: Didomi and the Privacy Regulation is: CCPA. Total HTTP Records represents the total number of HTTP records collected in this settings. Total HTTP Chains represents the number of chains we built using collected HTTP data. Syncing Events represents the number ofchains containing the data sharing. All data are from settings including removing cookies. We can analyze the data from both setting 1 and setting 2. There are minimal diferences observed in both Opt Out and Opt In settings.

<table><tr><td colspan="7">Didomi</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>1954</td><td>295</td><td>136427</td><td>1718</td><td>255</td><td>130499</td></tr><tr><td>1</td><td>1862</td><td>235</td><td>128373</td><td>1933</td><td>267</td><td>132669</td></tr><tr><td>2</td><td>1554</td><td>271</td><td>130922</td><td>1858</td><td>245</td><td>125409</td></tr><tr><td>3</td><td>1760</td><td>234</td><td>127028</td><td>1491</td><td>244</td><td>132634</td></tr><tr><td>4</td><td>2329</td><td>312</td><td>139056</td><td>2279</td><td>330</td><td>134956</td></tr><tr><td>5</td><td>1951</td><td>226</td><td>127350</td><td>2042</td><td>305</td><td>134851</td></tr></table>

Table 11: The number ofevents and data through HTTP data. The CMP is: Didomi and the Privacy Regulation is: GDPR. Total HTTP Records represents the total number of HTTP records collected in this settings. Total HTTP Chains represents the number of chains we built using collected HTTP data. Syncing Events represents the number ofchains containing the data sharing. All data are from settings including removing cookies. We can analyze the data from both setting 1 and setting 2. There are minimal diferences observed in both Opt Out and Opt In settings.

<table><tr><td colspan="7">Didomi</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>833</td><td>31</td><td>121457</td><td>937</td><td>42</td><td>123001</td></tr><tr><td>1</td><td>871</td><td>31</td><td>127088</td><td>737</td><td>14</td><td>122245</td></tr><tr><td>2</td><td>880</td><td>37</td><td>130116</td><td>838</td><td>25</td><td>125372</td></tr><tr><td>3</td><td>753</td><td>19</td><td>121093</td><td>783</td><td>21</td><td>125504</td></tr><tr><td>4</td><td>899</td><td>38</td><td>132361</td><td>865</td><td>35</td><td>129829</td></tr><tr><td>5</td><td>841</td><td>46</td><td>122519</td><td>837</td><td>19</td><td>126583</td></tr></table>

Table 12: The number ofevents and data through HTTP data. The CMP is: Quantcast and the Privacy Regulation is: CCPA. Total HTTP Records represents the total number ofHTTP records collected in this settings. Total HTTP Chains represents the number ofchains we built using collected HTTP data. Syncing Events represents the number ofchains containing the data sharing. All data are from settings including removing cookies. We can analyze the data from both setting 1 and setting 2. There are minimal diferences observed in both Opt Out and Opt In settings

<table><tr><td colspan="7">Quantcast</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>1862</td><td>302</td><td>71655</td><td>2252</td><td>319</td><td>72382</td></tr><tr><td>1</td><td>2132</td><td>346</td><td>75336</td><td>1409</td><td>192</td><td>68125</td></tr><tr><td>2</td><td>2050</td><td>343</td><td>71439</td><td>1674</td><td>288</td><td>70305</td></tr><tr><td>3</td><td>2040</td><td>362</td><td>74835</td><td>1767</td><td>299</td><td>69467</td></tr><tr><td>4</td><td>1751</td><td>281</td><td>68387</td><td>1740</td><td>268</td><td>67718</td></tr><tr><td>5</td><td>2136</td><td>343</td><td>71491</td><td>1995</td><td>287</td><td>71945</td></tr></table>

Table 13: The number ofevents and data through HTTP data. The CMP is: Quantcast and the Privacy Regulation is: GDPR. Total HTTP Records represents the total number of HTTP records collected in this settings. Total HTTP Chains represents the number of chains we built using collected HTTP data. Syncing Events represents the number of chains containing the data sharing. All data are from settings including removing cookies. A significant diference of syncing events was noticed in both Opt Out and Opt In settings when comparing settings 2 and 1, suggesting that fingerprint changes may afect the tracking.

<table><tr><td colspan="7">Quantcast</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>1077</td><td>42</td><td>67150</td><td>1130</td><td>44</td><td>68512</td></tr><tr><td>1</td><td>1150</td><td>47</td><td>70839</td><td>1095</td><td>49</td><td>65670</td></tr><tr><td>2</td><td>1184</td><td>97</td><td>67300</td><td>1261</td><td>66</td><td>69702</td></tr><tr><td>3</td><td>1033</td><td>41</td><td>65206</td><td>994</td><td>38</td><td>65513</td></tr><tr><td>4</td><td>1118</td><td>50</td><td>65522</td><td>980</td><td>34</td><td>63184</td></tr><tr><td>5</td><td>1067</td><td>28</td><td>65243</td><td>1012</td><td>30</td><td>63984</td></tr></table>

Table 14: The number ofevents and data through HTTP data. The CMP is: NAI and the Privacy Regulation is: CCPA. Total HTTP Records represents the total number ofHTTP records collected in this settings. Total HTTP Chains represents the number ofchains we built using collected HTTP data. Syncing Events represents the number ofchains containing the data sharing. All data are from settings including removing cookies. We can analyze the data from both setting 1 and setting 2. There are minimal diferences observed in Opt In setting. A significant diference was noticed in the Opt Out setting when comparing settings 2 and 1, suggesting that fingerprint changes may afect the tracking.

<table><tr><td colspan="7">NAI</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>949</td><td>203</td><td>32213</td><td>484</td><td>93</td><td>26908</td></tr><tr><td>1</td><td>600</td><td>149</td><td>27918</td><td>913</td><td>234</td><td>30701</td></tr><tr><td>2</td><td>1985</td><td>414</td><td>36313</td><td>971</td><td>211</td><td>29159</td></tr><tr><td>3</td><td>744</td><td>241</td><td>29736</td><td>1102</td><td>296</td><td>35130</td></tr><tr><td>4</td><td>1459</td><td>253</td><td>32307</td><td>1083</td><td>232</td><td>30027</td></tr><tr><td>5</td><td>1640</td><td>394</td><td>35534</td><td>1404</td><td>313</td><td>36936</td></tr></table>

Table 15: The number ofevents and data through HTTP data. The CMP is: NAI and the Privacy Regulation is: GDPR. Total HTTP Records represents the total number ofHTTP records collected in this settings. Total HTTP Chains represents the number ofchains we built using collected HTTP data. Syncing Events represents the number of chains containing the data sharing. All data are from settings including removing cookies. A significant diference was noticed in both Opt Out and Opt In settings when comparing settings 2 and 1, suggesting that fingerprint changes may afect the tracking.

<table><tr><td colspan="7">NAI</td></tr><tr><td></td><td colspan="3">Opt Out</td><td colspan="3">Opt In</td></tr><tr><td></td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td><td>HTTP Chains</td><td>Syncing Events</td><td>HTTP Records</td></tr><tr><td>0</td><td>153</td><td>27</td><td>26855</td><td>378</td><td>51</td><td>34869</td></tr><tr><td>1</td><td>159</td><td>27</td><td>28697</td><td>202</td><td>33</td><td>31542</td></tr><tr><td>2</td><td>371</td><td>132</td><td>30118</td><td>420</td><td>96</td><td>30925</td></tr><tr><td>3</td><td>255</td><td>34</td><td>34368</td><td>173</td><td>40</td><td>29926</td></tr><tr><td>4</td><td>168</td><td>18</td><td>25830</td><td>305</td><td>54</td><td>29436</td></tr><tr><td>5</td><td>152</td><td>37</td><td>25767</td><td>140</td><td>16</td><td>26178</td></tr></table>