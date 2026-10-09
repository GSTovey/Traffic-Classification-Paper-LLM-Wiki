# A Measurement of Genuine Tor Traces for Realistic Website Fingerprinting

Rob Jansen†

Ryan Wails†‡

Aaron Johnson†

†U.S. Naval Research Laboratory, ‡Georgetown University

## ABSTRACT

Website fingerprinting (WF) is a dangerous attack on web privacy because it enables an adversary to predict the website a user is visiting, despite the use of encryption, VPNs, or anonymizing networks such as Tor. Previous WF work almost exclusively uses synthetic datasets to evaluate the per formance and estimate the feasibility of WF attacks despite evidence that synthetic data misrepresents the real world. In this paper we present GTT23, the first dataset of genuine Tor traces, which we obtain through a large-scale measurement of the Tor network and which is intended especially for WF. It represents real Tor user behavior better than any existing WF dataset, is larger than any existing WF dataset by at least an order of magnitude, and will help ground the future study of realistic WF attacks and defenses. In a detailed evaluation, we survey 28 WF datasets published since 2008 and compare their characteristics to those of GTT23. We discover common deficiencies of synthetic datasets that make them inferior to GTT23 for drawing meaningful conclusions about the efectiveness of WF attacks directed at real Tor users. We have made GTT23 available to promote reproducible research and to help inspire new directions for future work.

## 1 INTRODUCTION

Website fingerprinting (WF) is a dangerous attack on web privacy because it enables an adversary that can observe a user’s outgoing connections to predict the website the user is visiting [6, 18, 19, 30, 51], even if those connections are protected with encryption, virtual private networks (VPNs), or anonymizing networks such as Tor [15]. WF attacks are particularly serious against Tor because they can break Tor’s anonymity [5, 9–11, 13, 17, 25, 36–39, 42–45, 47, 48, 56, 57, 59].

Consistent with previous WF work, we consider an adversary that uses machine learning (ML) to carry out WF attacks against Tor users from a vantage point on the entry side of the Tor network. In using ML for WF, accurately labeled traces (i.e., examples) are required (1) to train WF classifiers to form correct associations between encrypted trafic patterns and destination websites, and (2) to evaluate classifier eficacy. A major problem for the adversary is that information about the destination website needed to label the traces is encrypted by Tor’s onion routing scheme [52] when observed from the entry position. Thus, the adversary needs some other method to collect labeled traces.

Through a survey of 28 WF datasets published since 2008 (see § 4), we find that all but a single prior study consider an adversary that collects labeled traces using an automated browser that programmatically fetches a set of selected webpages through Tor [2]. Such synthetic datasets have been criticized as unrepresentative of genuine Tor trafic along numerous axes [25, 29, 40, 44], and their use has led WF research to fall victim to several common ML evaluation pitfalls such as the base rate fallacy [3, 10, 29].

In an efort to address the serious limitations of synthetic WF datasets, a recent study by Cherubin et al. [10] considers a WF strategy in which the adversary uses a Tor exit relay to collect genuine traces, which can be observed and labeled by a relay in the exit position. Genuine traces exhibit the real-world diversity in all factors that might influence classifier performance, and they enable researchers to more accurately evaluate the WF performance that we expect an adversary might realistically attain. Unfortunately, this prior study was done in a fully online setting in order to avoid persistently storing genuine data or trained WF classifiers. As a result, it is impossible to replicate their results, and it is dificult to build on the methodology. Indeed, many later works have continued to study WF using synthetically generated datasets [4, 13, 25, 31, 33, 45].

In this paper we present GTT23, the first dataset of labeled genuine Tor traces. We describe a large-scale Tor relay measurement plan that we designed to prioritize safety and privacy, which we developed through consultation with our organization’s Institutional Review Board and with the Tor Research Safety Board [54]. We executed our reviewed measurement process to safely measure 13,900,621 circuits to 1,142,115 unique destination domains and 68 unique destination server ports during a 13-week measurement period. We analyze GTT23 and find that 96% of the measured circuits use ports 80, 8080, or 443 to first connect to a destination, that most of the measured circuits carry fewer than 25 cells (<10.5 KB), and that just a single circuit was measured for over 80% of the measured domains. Our analysis of GTT23 helps demonstrate the high degree of trafic diversity with which a WF adversary must contend when launching WF attacks in the real world.

We further evaluate GTT23 to compare its genuine characteristics to those of existing synthetic WF datasets. First, we survey 28 WF datasets published since 2008 and identify several common deficiencies of synthetic datasets. We find that synthetic datasets are composed of a single trafic type (web) using simplistic user models and static software tools while focusing on website index pages at uninformed base rates. Second, we conduct a detailed analysis of the statistical disparities between GTT23 and two recent synthetic datasets that are specifically designed for more complex website fingerprinting wherein a website contains multiple accessible webpages. We find that the circuit-length variation and website base rates are still not reflected well in the synthetic datasets despite the improved modeling.

We conclude that, because GTT23 contains genuine traces of websites accessed by real Tor users at natural base rates, it is more realistic than any existing synthetic dataset, and thus it will enable WF evaluations that more accurately estimate real-world WF performance. We also note that, while GTT23 was designed to facilitate WF research, it may be useful for other research on Tor trafic analysis, such as correlation attacks [35] or malware detection [16].

This dataset has been available to researchers upon request since 2024 [27]. This report contains details and analyses of the data to further the understanding and use of GTT23 and to promote the development of similar datasets. It is a full version of the conference paper [26], adding Listing 1, Table 1, Appendix A, and some additional details throughout.

## 2 METHODOLOGY

## 2.1 Background

Tor [15] uses onion routing to anonymize TCP connections on the Internet. The Tor network consists of a globally distributed set of relays. Each connection through Tor to an outside server is sent through a three-hop circuit. This design is intended to prevent an adversary observing any single relay, or one observing either the client or destination but not both, from being able to identify both the source and destination of a connection. In the Tor network today, there are currently over 8,500 relays and over 3 million daily users [53].

To use Tor, a client builds circuits, each passing through an entry, a middle, and an exit relay. Each circuit supports multiplexing multiple streams of end-to-end TCP communication with internet services. When a new TCP connection to a service is requested by an application (e.g., Tor Browser), the Tor client will use fixed-size application-layer control messages called cells to instruct the exit relay to (1) resolve the service’s domain name, and (2) make a TCP connection to the service. Each of a circuit’s TCP byte-streams is subsequently forwarded bidirectionally through the circuit in data cells. Circuit trafic observed from a single network location can be represented as a time-ordered sequence of (direction, time) pairs (one for each cell sent through a circuit), which we call a cell trace.

A TCP stream may be assigned to any circuit with an exit relay that allows connection to the destination’s IP address and port; if no such circuit exists, a new one is built after choosing an exit independently at random from among those with conforming exit policies and weighted by relay bandwidth to balance load. However, Tor Browser employs additional stream assignment rules. When loading a webpage URL, Tor Browser computes the URL’s first-party domain name (FPDN) and instructs the Tor client to assign all streams created to load that URL (including those to third-party domains to load embedded objects) on a circuit uniquely associated with the FPDN and isolated from other streams.

Browsing to a page of a new website in Tor Browser will result in a unique FPDN and a new circuit tasked with first resolving a DNS query for the FPDN and then loading the page, while subsequent subpages of that website will be loaded through the same circuit. Cherubin et al. thus recognized that (1) the FPDN in the circuit’s first DNS query can be used to label the website of a circuit’s cell trace, and (2) an adversary running exit relays can observe genuine cell traces and their domain name labels, which can be used to train WF classifiers and produce more realistic estimates of WF performance [10]. (Non-exit relays can observe cell traces but not domain names due to onion routing [52].) Unfortunately, their study considered a fully online setting to avoid persistently storing genuine data or trained WF classifiers; thus a new measurement is needed to build on the methodology.

In WF, an adversary uses the volume and timing of trafic to infer which website is being visited [29]. This attack is suited to breaking the privacy of trafic sent through VPNs or Tor because their trafic plaintext and destination are unobservable. In a WF attack, the adversary observes the client and its trafic. Typical WF attacks use machine-learning classifiers trained on trafic traces labeled with the destination website (e.g., [11, 45, 47]). The classifiers are applied to trafic traces from the target client to identify the destination website. In the Tor setting, unlike for VPN trafic, WF classifiers are typically only given when a cell appears and in which direction because of Tor’s fixed-size cells, which can either be recorded directly by a malicious Tor relay or reconstructed from TCP packet payloads by a network observer.

## 2.2 Measurement Process

We designed a measurement process that employs one or more Tor exit relays to safely measure genuine Tor cell traces and FPDN labels. The traces and labels are collected into a dataset for subsequent analysis. Each participating relay runs a patched version of Tor that we modified to support our measurement as follows.

2.2.1 Circuit Selection. When a relay observes a new circuit, it rejects any non-exit type circuit (i.e., onion-service and internal circuits) from measurement. Additionally, the relay applies a probabilistic sampling procedure such that 80% of exit-type circuits are rejected during high-volume measurement intervals, and 98% of exit-type circuits are rejected during low-volume measurement intervals. Sampling helps us limit the total amount of data collected and provides plausible deniability: any individual circuit created through a participating relay is unlikely to exist in the dataset. Nonrejected circuits are selected for further measurement.

2.2.2 Circuit Measurement. A relay internally stores circuit metadata and cell traces during operation for the randomly <sup>selected</sup> <sup>exit-type</sup> <sup>circuits.</sup> <sup>We</sup> <sup>use</sup> <sup>an</sup> <sup>encoding</sup> <sup>function �</sup>(�) to protect some of this metadata:

$$
H ( x ) = { \mathrm { b a s e } } 6 4 { \mathrm { e n c o d e } } ( { \mathrm { s h a } } 2 5 6 ( x | | s a l t ) )\tag{1}
$$

where salt is chosen uniformly at random, fixed on all measurement relays for the duration of the measurement period, and then destroyed. Tor’s existing internal implementations are used for the base64encode and sha256 functions. The relay iteratively constructs a circuit metadata record for each selected circuit (applying � to domain names) until either the circuit closes or � cells have been observed, whichever occurs first.<sup>1</sup> The metadata record is then exported via Tor’s control interface to an external process that compresses it, encrypts it with a public-key encryption scheme, and writes it to persistent storage.

Each metadata record includes the following as exemplified in Listing 1: (1) day: an integer number of days that have elapsed since the start of the measurement; (2) domain: � � where � is the domain name of the circuit’s first exit <sup>stream;3 (3)</sup> <sup>shortest\_private\_sufix:</sup> <sup>�</sup>(�) <sup>where</sup> � <sup>is</sup> <sup>the</sup> <sup>short-</sup> est private sufix of the pre-image of domain computed using Mozilla’s public sufix list and libpsl [7]; (4) port: the server port used when connecting the circuit’s first exit stream to its destination; and (5) cells: a list of at most � cell metadata items. Each cell metadata item is a 4-tuple containing the time the cell was observed relative to the circuit’s creation time, an integer encoding the cell’s direction, and two integers encoding the cell and relay command, respectively [14].

## 2.3 Safety and Ethical Considerations

Our measurement process was designed to prioritize safety and privacy and was developed through consultation with

## Listing 1: Example circuit metadata record.

```json
{
" d a y " : 2 ,
" domain " : Dnqty37vYTIEivWhAEikb7HlJOzWXEZ2Rw05iicG7e8 ,
" s h o r t e s t _ p r i v a t e _ s u ffi x " :
bIKFK8gYicwptEMM1Goxlo7KredMMFx48VD0MpXn9zc ,
" p o r t " : 4 4 3 ,
" c e l l s " : [
[ 0 . 0 0 0 0 1 5 , 1 , 10 , 0 ] , / / c l i e n t −> e x i t : c r e a t e
[ 0 . 0 0 0 4 6 3 , −1 , 11 , 0 ] , / / e x i t −> c l i e n t : c r e a t e d
[ 1 0 . 9 3 2 3 4 0 , 1 , 9 , 1 ] , / / c l i e n t −> e x i t : r e l a y _ e a r l y . b e g i n
[ 1 2 . 0 7 0 9 5 4 , −1 , 3 , 3 ] , / / e x i t −> c l i e n t : r e l a y . c o n n e c t e d
[ 1 3 . 4 2 1 0 1 7 , 1 , 9 , 2 ] , / / c l i e n t −> e x i t : r e l a y _ e a r l y . d a t a
[ 1 3 . 4 2 1 0 3 0 , −1 , 3 , 2 ] , / / e x i t −> c l i e n t : r e l a y . d a t a
]
}
```

our organization’s Institutional Review Board (IRB) and the Tor Research Safety Board (TRSB) [54]. Our IRB qualified our study as non-human-subject research, and our TRSB interaction resulted in a “No Objections” score and instructions to move forward with our plans. Extended analysis ofthe safety, risks, and benefits of our measurement and details about IRB and TRSB interactions are provided in Appendix A.

## 3 MEASUREMENT AND ANALYSIS

## 3.1 Measurement Details

We execute a large-scale Tor measurement study following our methodology from § 2. First, we run a total of eight exit relays, four on each of two identical machines hosted by the Calyx Institute (a nonprofit research and education organization located in NY, USA). Each machine is equipped with 2 Intel Xeon E5-2695 v2 12-core CPUs (48 hyper-threads in total) and connected to an unmetered 1 Gbit/s symmetric network access link. Second, we run a measurement over a 13 week period in 2023; we assign weeks 1, 7, and 13 as high-volume intervals, and the remaining 10 weeks as lowvolume intervals. We combined all recorded circuit metadata records into a single dataset which we call GTT23 [27].

## 3.2 Data Analysis

In total, GTT23 contains 13,900,621 circuits, 10,557,898 of which were observed during the high-volume weeks (1, 7, and 13) and 3,342,723 of which were observed during the remaining 10 low-volume weeks.

The daily total and weekly mean number of GTT23 circuits are shown in Fig. 1; the daily mean during high-volume weeks is 502,757 and the daily mean during low-volume weeks is 47,753. We observe a slight increase in circuit counts during the latter half of the measurement period which we attribute to natural fluctuation in network usage and the load-balancing weights used for relay selection.

![](images/a267621cf0a8913b9de247b49c1412edf57b7772603b3ccaac2473e214db6082.jpg)  
Figure 1: The daily total (bars) and weekly mean (text) number of circuits during our 13 week measurement.

![](images/3a89a62d9cfc3aa4c1662890a0bc91c31bb366e94c4154bf2b522ac2ed6b2653.jpg)  
Figure 2: The total number of GTT23 circuits by server port, with IANA-assigned service names [55].

GTT23 contains circuits measured across 68 unique destination server ports. The distribution of the number of measured circuits across the top-ten most-popular service ports is shown in Fig. 2 (with a logarithmic x-axis, and the IANAassigned service names shown in the legend). We observe that 13,356,305 circuits (96%) use ports 80, 8080, or 443 to connect their first stream to a destination service; these ports are assigned to HTTP and HTTPS by the IANA [55]. The vast majority of the remaining circuits use port 43 or 4321, which are respectively assigned to WhoIs and Remote WhoIs services by the IANA. Frequent connections to these ports have been observed in prior studies of Tor exit trafic [49, 50]: Sonntag observed that they corresponded to a large number of reverse DNS lookups scanning several large networks [49].

The cumulative distribution of the number of observed cells per GTT23 circuit is shown in Fig. 3. We were surprised to find that most circuits are extremely short: the median number of cells over all circuits is just 25, which would support at most 10.5 KB of application payload after accounting for control cells and cell-header overhead. For comparison, we also plot in Fig. 3 the circuit length distribution for the subsets of circuits containing at least 25, 100, and 1,000 cells, respectively corresponding to 10.5, 47.8, and 496 KB of application payload. For reference, the HTTP Archive reports that over 90% of webpages have a transfer size greater than 450 KB across samples of 12 and 16 million desktop and mobile URLs, respectively (see Table 1). Thus, we believe that most GTT23 circuits did not carry full webpage transfers.

![](images/47f1f53a4f26960e83ac9f46c3bd7a5d3fa0906c2462fd9c8243c9ea8d9bf45c.jpg)  
Figure 3: Cumulative distribution of the number of cells per circuit over subsets of GTT23 circuits.

Table 1: Total Web Page Transfer Size (KB) in 2023-08†
<table><tr><td>Client</td><td>Percentile:</td><td>10th</td><td>25th</td><td>50th</td><td>75th</td><td>90th</td></tr><tr><td>Desktop</td><td></td><td>547</td><td>1,226</td><td>2,484</td><td>4,967</td><td>9,744</td></tr><tr><td>Mobile</td><td></td><td>457</td><td>1,063</td><td>2,179</td><td>4,377</td><td>8,946</td></tr></table>

† HTTP Archive: https://httparchive.org/reports/state-of-the-web

![](images/1d90e4210848f0a3bce0291f83db5b572d6c99b961bde7b8f002cbdbec9e869a.jpg)  
Figure 4: The number of GTT23 circuits per domain; we observe a close fit to a power-law distribution.

GTT23 contains circuits measured across 1,142,115 unique destination domains. The distribution of the number of measured circuits per domain is plotted in Fig. 4. We observe a close fit to a power-law distribution (shape=0.023, loc=0.769, scale=1,495,234), where few popular domains dominate the measurement while a long tail exists with just a single circuit measured for 908,422 (80%) of the domains.

Note that obtaining realistic base rates for the domains visited by Tor users is a major advantage of GTT23 over synthetic datasets. In open-world binary classification, the negative class is composed of traces to all sites other than the monitored ones. Thus, the false-positive rate, which is crucial for estimating precision [56], depends on the base rates in the negative class. Similarly, in a multiclass setting (open or closed world), overall WF accuracy depends on the base rates of each class.

![](images/b018df76fd0a326aab49c7d16982e5318c2b6f179f51f56c591181b4973e1968.jpg)  
Figure 5: Cumulative distribution of circuit length variation across domains with at least two GTT23 circuits.

Fig. 5 shows the cumulative distribution of two measures of circuit length variability for each domain with more than one GTT23 circuit. The median Coeficient of Variation (i.e., the standard deviation divided by the mean) shows that more than half of the domains have a circuit length standard deviation greater than the mean, while the Coeficient of Dispersion (i.e., the variance divided by the mean) shows that most domains have a relative variance in circuit lengths of multiple hundreds of cells. The high variability in circuit lengths is consistent with our prior observation that most of the measurement circuits are short, and suggests that many Tor circuits may completely or prematurely fail.

## 4 EVALUATION

In this section, we compare GTT23 and synthetic datasets to understand how well the synthetic datasets model some of the genuine data characteristics that are important for WF.

## 4.1 Deficiencies of Synthetic Datasets

We survey 28 datasets proposed for WF tasks covering the years 2008–2025 In Table 2 we provide an overview of the properties of a subset of the surveyed datasets, selected for their size, complexity, and frequency with which they are used to evaluate later attacks. See Table 3 in Appendix B for the full comparison.

Like GTT23, these datasets also consist of Tor trafic traces labeled with a destination domain, and they record trafic that actually transited the Tor network and connected to some third-party server. However, we find that every dataset exhibited similar deficiencies: (1) they consist of only web trafic; (2) they are collected using simplistic user models and static software tools, almost exclusively at the client position; (3) they primarily focus on fetching popular webpages; and (4) they do not contain informed base rates. In contrast, real Tor clients use a wide variety of software and software versions, interact with non-web services, and do more than just non-interactively fetch selected webpages. These deficiencies make it dificult to use existing datasets to draw meaningful conclusions about the efectiveness of a WF attack directed at real Tor users [10, 29].

Table 2: Select WF Datasets (full details in Table 3)
<table><tr><td>Dataset</td><td>Year</td><td>Size</td><td>Description†</td></tr><tr><td>k-NN [57]</td><td>2014</td><td> $1 . 4 \times 1 0 ^ { 4 }$ </td><td>Web, top index pages</td></tr><tr><td>AWF  $C W _ { 9 0 0 }$  [44]</td><td>2017</td><td> $2 . 3 \times 1 0 ^ { 6 }$ </td><td>Web, top index pages</td></tr><tr><td>AWF Open [44]</td><td>2017</td><td> $8 \ \times 1 0 ^ { 5 }$ </td><td>Web, top index pages</td></tr><tr><td>DF [47]</td><td>2018</td><td> $1 . 4 \times 1 0 ^ { 5 }$ </td><td>Web, top index pages</td></tr><tr><td>GoodEnough [41] 2020</td><td></td><td> $2 \ \times 1 0 ^ { 4 }$ </td><td>Web, top index pages + subpages</td></tr><tr><td>BigEnough [33]</td><td>2021</td><td> $3 . 8 \times 1 0 ^ { 4 }$ </td><td>Web, top index pages + subpages</td></tr><tr><td>Multi-tab [13]</td><td>2022</td><td> $5 . 7 \times 1 0 ^ { 5 }$ </td><td>Web, top index pages, multiple tabs</td></tr><tr><td>GTT23</td><td>2023</td><td> $1 . 4 \times 1 0 ^ { 7 }$ </td><td>Genuine traffic, real user behavior, visited services, natural base rates</td></tr></table>

† All but GTT23 synthetically fetch webpages using automated tools.

In comparison, GTT23 is the only dataset with traces sampled from genuine trafic created by real Tor users interacting with real internet services at natural base rates. GTT23 is not limited to only web trafic: it contains traces of diferent types of internet activity and supports the evaluation of WF attacks and defenses based on websites’ first-party domain names (see §2.1). These traces better represent the WF problem, where an adversary observes undiferentiated trafic from real users and cannot assume that the trafic is just to index web pages or is even to a website at all. Thus, GTT23 can serve to more accurately evaluate the threat posed by a real-world WF adversary. Moreover, GTT23 is larger than the previous largest dataset (Rimmer et al.’s AWF dataset [44]) by an order of magnitude which is important to assess modern deep learning attacks requiring many training examples. Extended results and analysis from our dataset survey appear in Appendix B.

## 4.2 Genuine and Synthetic Disparities

We analyze the statistical disparities between GTT23 and synthetic datasets to understand dataset quality. We place particular emphasis on the trace features found in prior work [17] to be informative for WF. We focus our analysis on two recent synthetic datasets, BigEnough [33] and GoodEnough [41], that were specifically designed to model website fingerprinting; both datasets contain at least ten pages per website and so they represent among the highest website diversity of the datasets surveyed.

![](images/6c781278e5362a15b53e25598358d4c281e069d34d2fdeccb43e559b11789ff8.jpg)

![](images/6f0c1ca183bcbf2992f09ce33a9cbeae98e682118df01ca281d50183e8c5b701.jpg)

![](images/5ef061318c9836f6e119a7b9f2f91f011e4d2347e45ccca0c3ede0e73945c87a.jpg)  
Figure 6: Per-domain statistics computed from the GTT23, BigEnough [33], and GoodEnough [41] datasets. For statistical rigor, here we consider traces with at least 1,000 cells and, among those, domains with at least 30 traces.

4.2.1 Dataset Composition. The GTT23 dataset contains traces generated from real users interacting with any services accessible via the internet (including non-web services), whereas synthetic datasets such as BigEnough and Good Enough contain traces generated from automated visits to small number of popular websites. Empirical data from this work and previous work suggests that Tor users do not just visit popular websites. First, Fig. 2 shows that a long tail ( 4%) of GTT23 traces are generated from interactions with hosts not running on known web ports such as 80, 443, or 8080. Second, a privacy-preserving measurement of the Tor network performed in 2018 [32] determined that over 20% of web streams exiting the Tor network access a host not in the Alexa Top 1 Million list. This long tail of activity is not reflected in the synthetic datasets and is likely to make the WF classification task more dificult [38].

4.2.2 Data Modeling. Even simple features computed from the synthetic datasets do not accurately model genuine Tor traces. Consider, for example, overall trace length, a feature shown in prior work to be informative in the WF task [17]. The leftmost plot in Fig. 6 shows, for all 3 datasets, the distribution of each domain’s median circuit length (cell count) for circuit traces with at least 1,000 cells and among those, domains with at least 30 traces. The plot shows that GTT23 traces tend to be shorter than synthetic dataset traces. Good-Enough traces, in particular, tend to be much longer than genuine traces: roughly 70% of GoodEnough domains have a median circuit length of 5,000 cells (the capture limit), whereas this is true of only 32% of domains in the GTT23 dataset. Inaccurate data modeling makes it dificult to draw meaningful conclusions from the synthetic datasets [3].

4.2.3 Intra-class Variance. Genuine user traces contain a much richer set of activity than is generated by synthetic, automated crawls to webpages. Genuine traces may be generated from various unpredictable user-initiated behaviors and processes and may reflect complex, interactive sessions with internet hosts, whereas synthetic traces are usually generated by a single, fixed crawling application such as tor-browser-selenium [2] and are limited to simple page accesses. The center plot in Fig. 6 shows the distribution of the coeficient of variation of trace length—that is, the ratio of the trace length’s standard deviation to the mean—across the domains of each dataset. At nearly every percentile, the coeficient is higher for GTT23 domains than it is for BigEnough and GoodEnough domains, suggesting that GTT23 traces exhibit higher variation. The higher variance for each domain suggests that WF is more dificult on genuine than on synthetic traces.

4.2.4 Base Rates. Recall that the frequency of website occurrence in the GTT23 dataset is characterized by a few heavy hitters and a long tail of rarely accessed sites (see Fig. 4). In contrast, the rightmost plot of Fig. 6 shows that most domains in the synthetic datasets occur with much higher frequency. For example, the median domain occurs with frequency $5 \times 1 0 ^ { - 4 }$ in GTT23. In comparison, the median domain in the BigEnough and GoodEnough dataset occur with frequencies that are orders-of-magnitude greater, $1 \times 1 0 ^ { - 2 }$ and $4 \times 1 0 ^ { - 3 }$ . Base rate realism is an important aspect of evaluating WF attacks because increasingly low false positive rates are needed to maintain precision at low base rates of occurrence [8, 29, 56]. Precisely fingerprinting most websites in GTT23 requires orders-of-magnitude lower false positives rates compared to BigEnough and GoodEnough.

## 5 CONCLUSION AND FUTURE WORK

Our goal in this work is to ground the future study of realistic WF attacks and defenses while promoting reproducible research. Toward this goal, we designed a safe Tor measurement methodology through consultation with the TRSB [54] and our institution’s IRB. We executed the methodology across eight Tor exit relays to measure $^ { 1 3 , 9 0 0 , 6 2 1 }$ circuits and compose GTT23, the first dataset of genuine Tor traces. We analyze GTT23 to better understand the characteristics of genuine Tor data, and evaluate the extent to which existing synthetic WF datasets misrepresent genuine characteristics.

We conclude that, because GTT23 contains genuine traces of websites accessed by real Tor users at completely natural base rates, it is more realistic than any existing synthetic dataset and thus it will enable WF evaluations that more accurately estimate real-world WF performance.

GTT23 has been available to researchers upon request since 2004 since [27], and it has already been used to improve our understanding of WF on Tor. Jansen et al. [28] develop the Retracer methodology for performing WF analysis on Tor trace datasets that, like GTT23, are collected at the exit relay. Retracer modifies the trafic traces to appear more as they would to an adversary observing the client. The results indicate that a WF adversary is likely to obtain much lower accuracy than synthetic datasets have indicated. Jansen [20] further develops this methodology. Similarly, Deng et al. [12] use GTT23 to perform a WF analysis where the adversary is detecting connections to a monitored set of sites. Their results indicate that the Var-CNN classifier obtains higher accuracy than the DF classifier used by Jansen et al.

GTT23 can be used to conduct both training and testing of WF classifiers in either an ofline or an online streaming model. During training, GTT23 can provide genuine examples not only of a target class of websites, but also of the background class; negative class examples are important for training classifiers to be robust against the high-diversity WF patterns we find in practice. However, it is even more important to incorporate genuine traces while testing WF classifiers to accurately represent the challenge facing a real world adversary deploying an attack. Future work should consider new WF classification techniques that are specifically developed and tuned to genuine traces to further improve our understanding of the real world WF performance an adversary can expect to attain.

One limitation of GTT23 is that the labels were created by randomizing website domains with an irreversible hash function due to privacy and ethical requirements. While this may seem to inhibit our ability to synthesize GTT23 with other labeled datasets, many emerging self-supervised ML training methods [4, 36, 48] have unsupervised pre-training phases that learn how to generally diferentiate websites without the need for labels. Such approaches could leverage GTT23 for pre-training to benefit from the genuine patterns it contains, and then use a diferent labeled dataset with many fewer traces for fine-tuning the pre-trained models.

There are also applications outside ofWF. The trafic statistics of GTT23 regarding Tor usage are of independent interest, since previous Tor measurement studies are already outdated by more than five years [24, 32]. Additionally, GTT23 could be used to enhance the realism and fidelity of Tor network testbeds and simulations [22, 23] since the traces encode the timing and patterns of genuine user activities.

## ACKNOWLEDGMENTS

This work was supported by the Ofice of Naval Research (ONR).

## REFERENCES

[1] Kota Abe and Shigeki Goto. 2016. Fingerprinting attack on Tor anonymity using deep learning. APAN, 42.

[2] Gunes Acar, Marc Juarez, and individual contributors. 2023. Torbrowser-selenium - Tor browser automation with Selenium. https ://github.com/webfp/tor-browser-selenium. (2023).

[3] Daniel Arp, Erwin Quiring, Feargus Pendlebury, Alexander Warnecke, Fabio Pierazzi, Christian Wressnegger, Lorenzo Cavallaro, and Konrad Rieck. 2022. Dos and don’ts of machine learning in computer security. In USENIX Security 2022. (2022).

[4] Alireza Bahramali, Ardavan Bozorgi, and Amir Houmansadr. 2023. Realistic website fingerprinting by augmenting network traces. In ACM CCS 2023. (2023). doi:10.1145/3576915.3616639.

[5] Sanjit Bhat, David Lu, Albert Kwon, and Srinivas Devadas. 2019. Var-CNN: A data-eficient website fingerprinting attack based on deep learning. PoPETs, 2019, 4, (2019). doi:10.2478/popets-2019-0070.

[6] George Dean Bissias, Marc Liberatore, David D. Jensen, and Brian Neil Levine. 2005. Privacy vulnerabilities in encrypted HTTP streams. In PET 2005. Vol. 3856. (2005). doi:10.1007/11767831\_1.

[7] 2023. C library for the public sufix list. https://github.com/rockdaboo t/libpsl. https://publicsuffix.org. (2023).

[8] Xiang Cai, Rishab Nithyanand, Tao Wang, Rob Johnson, and Ian Goldberg. 2014. A systematic approach to developing and evaluating website fingerprinting defenses. In ACM CCS 2014. (2014). doi:10.1145/266 0267.2660362.

[9] Xiang Cai, Xin Cheng Zhang, Brijesh Joshi, and Rob Johnson. 2012. Touching from a distance: website fingerprinting attacks and defenses. In ACM CCS 2012. (2012). doi:10.1145/2382196.2382260.

[10] Giovanni Cherubin, Rob Jansen, and Carmela Troncoso. 2022. Online website fingerprinting: evaluating website fingerprinting attacks on Tor in the real world. In USENIX Security 2022. (2022). eprint: https://w ww.usenix.org/conference/usenixsecurity22/presentation/cherubin.

[11] Xianwen Deng, Ruijie Zhao, Yanhao Wang, Mingwei Zhan, Zhi Xue, and Yijun Wang. 2025. Countmamba: a generalized website fingerprinting attack via coarse-grained representation and fine-grained prediction. In 2025 IEEE Symposium on Security and Privacy.

[12] Xinhao Deng, Jingyou Chen, Linxiao Yu, Yixiang Zhang, Zhongyi Gu, Changhao Qiu, Xiyuan Zhao, Ke Xu, and Qi Li. 2025. Beyond a single perspective: towards a realistic evaluation of website fingerprinting attacks. Tsinghua Science and Technology.

[13] Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, and Jianping Wu. 2023. Robust multi-tab website fingerprinting attacks in the wild. In 2023 IEEE Symposium on Security and Privacy. (2023). doi:10.1109/SP46215.2023.10179464.

[14] Roger Dingledine and Nick Mathewson. 2003. The Tor protocol specification. Accessed: September 30, 2023. https://gitlab.torproject.org/tp o/core/torspec/-/blob/main/tor-spec.txt.

[15] Roger Dingledine, Nick Mathewson, and Paul F. Syverson. 2004. Tor: the second-generation onion router. In USENIX Security 2004. (2004).

[16] Priyanka Dodia, Mashael AlSabah, Omar Alrawi, and Tao Wang. 2022. Exposing the rat in the tunnel: using trafic analysis for tor-based malware detection. In ACM CCS 2022. (2022).

[17] Jamie Hayes and George Danezis. 2016. �-fingerprinting: A robust scalable website fingerprinting technique. In USENIX Security 2016. (2016).

[18] Dominik Herrmann, Rolf Wendolsky, and Hannes Federrath. 2009. Website fingerprinting: attacking popular privacy enhancing tech nologies with the multinomial naïve-bayes classifier. In The Workshop on Cloud Computing Security.

[19] Andrew Hintz. 2002. Fingerprinting websites using trafic analysis. In PET 2002. Vol. 2482. (2002). doi:10.1007/3-540-36467-6\_13.

[20] Rob Jansen. 2026. CellShift: RTT-Aware Trace Transduction for Real-World Website Fingerprinting. In NDSS 2026. (2026). doi:10.14722/ndss .2026.231004.

[21] Rob Jansen. 2023. Constructing a real-world dataset for studying web site fingerprinting. (2023). https://lists.torproject.org/pipermail/tor-pr oject/2023-April/003604.html.

[22] Rob Jansen and Nicholas Hopper. 2012. Shadow: running Tor in a box for accurate and eficient experimentation. In NDSS 2012. (2012).

[23] Rob Jansen, Jim Newsome, and Ryan Wails. 2022. Co-opting linux processes for High-Performance network simulation. In USENIX ATC 2022. (2022). eprint: https://www.usenix.org/conference/atc22/prese ntation/jansen.

[24] Rob Jansen, Matthew Traudt, and Nicholas Hopper. 2018. Privacy preserving dynamic learning of tor network trafic. In ACM CCS 2018. doi:10.1145/3243734.3243815.

[25] Rob Jansen and Ryan Wails. 2023. Data-explainable website fingerprinting with network simulation. PoPETs, 2023, 4, (2023). doi:10.5655 3/popets-2023-0125.

[26] Rob Jansen, Ryan Wails, and Aaron Johnson. 2026. A measurement of genuine tor traces for realistic website fingerprinting. In Proceedings ofthe 27th Passive and Active Measurement Conference (PAM 2026).

[27] Rob Jansen, Ryan Wails, and Aaron Johnson. Gtt23: a 2023 dataset of genuine tor traces. Version 1.0.0. (2024). doi:10.5281/zenodo.10620520.

[28] Rob Jansen, Ryan Wails, and Aaron Johnson. 2023. Repositioning real-world website fingerprinting on tor. In WPES 2023.

[29] Marc Juárez, Sadia Afroz, Gunes Acar, Claudia Díaz, and Rachel Greenstadt. 2014. A critical evaluation of website fingerprinting attacks. In ACM CCS 2014. (2014). doi:10.1145/2660267.2660368.

[30] Marc Liberatore and Brian Neil Levine. 2006. Inferring the source of encrypted HTTP connections. In ACM CCS 2006. (2006). doi:10.1145/1 180405.1180437.

[31] Limam, Noura, Barradas, Diogo, Arun Naik, Shreya, Singh, Prabhjot, and Malekghaini, Navid. 2023. A first look at generating website fingerprinting attacks via neural architecture search. In WPES 2023.

[32] Akshaya Mani, T Wilson-Brown, Rob Jansen, Aaron Johnson, and Micah Sherr. 2018. Understanding Tor usage with privacy-preserving measurement. In ACM IMC 2018.

[33] Nate Mathews, James K Holland, Se Eun Oh, Mohammad Saidur Rahman, Nicholas Hopper, and Matthew Wright. 2023. SoK: a critical evaluation of eficient website fingerprinting defenses. In 2023 IEEE Symposium on Security and Privacy. (2023). doi:10.1109/SP46215.2023 .10179289.

[34] Asya Mitseva and Andriy Panchenko. 2024. Stop, don’t click here anymore: boosting website fingerprinting by considering sets of subpages. In USENIX Security 2024.

[35] Milad Nasr, Alireza Bahramali, and Amir Houmansadr. 2018. Deep-Corr: Strong Flow Correlation Attacks on Tor Using Deep Learning. In ACM CCS 2018. (2018).

[36] Se Eun Oh, Nate Mathews, Mohammad Saidur Rahman, Matthew Wright, and Nicholas Hopper. 2021. GANDaLF: GAN for data-limited fingerprinting. PoPETs, 2021, 2, (2021). doi:10.2478/popets-2021-0029.

[37] Se Eun Oh, Saikrishna Sunkam, and Nicholas Hopper. 2019. p-FP: extraction, classification, and prediction of website fingerprints with deep learning. PoPETs, 2019, 3, (2019). doi:10.2478/popets-2019-0043.

[38] Andriy Panchenko, Fabian Lanze, Jan Pennekamp, Thomas Engel, Andreas Zinnen, Martin Henze, and Klaus Wehrle. 2016. Website fingerprinting at internet scale. In NDSS 2016. (2016).

[39] Andriy Panchenko, Lukas Niessen, Andreas Zinnen, and Thomas Engel. 2011. Website fingerprinting in onion routing based anonymization networks. In WPES 2011.

[40] Mike Perry. 2013. A critique of website trafic fingerprinting attacks. https://blog.torproject.org/blog/critique-website-traffic-fingerprint ing-attacks.

[41] Tobias Pulls. 2020. Towards efective and eficient padding machines for tor. arXiv preprint arXiv:2011.13471.

[42] Tobias Pulls and Rasmus Dahlberg. 2020. Website fingerprinting with website oracles. PoPETs, 2020, 1, (2020). doi:10.2478/popets-2020-0013.

[43] Mohammad Saidur Rahman, Payap Sirinam, Nate Mathews, Kantha Girish Gangadhara, and Matthew Wright. 2020. Tik-Tok: the utility of packet timing in website fingerprinting attacks. PoPETs, 2020, 3, (2020). doi:10.2478/popets-2020-0043.

[44] Vera Rimmer, Davy Preuveneers, Marc Juárez, Tom van Goethem, and Wouter Joosen. 2018. Automated website fingerprinting through deep learning. In NDSS 2018. (2018).

[45] Meng Shen, Kexin Ji, Zhenbo Gao, Qi Li, Liehuang Zhu, and Ke Xu. 2023. Subverting website fingerprinting defenses with robust trafic representation. In USENIX Security 2023. (2023). eprint: https://www .usenix.org/conference/usenixsecurity23/presentation/shen-meng.

[46] Meng Shen, Jinhe Wu, Junyu Ai, Qi Li, Chenchen Ren, Ke Xu, and Liehuang Zhu. 2025. Swallow: a transfer-robust website fingerprinting attack via consistent feature learning. In ACM CCS 2025. (2025).

[47] Payap Sirinam, Mohsen Imani, Marc Juárez, and Matthew Wright. 2018. Deep fingerprinting: undermining website fingerprinting defenses with deep learning. In ACM CCS 2018. (2018). doi:10.1145/3243734.324 3768.

[48] Payap Sirinam, Nate Mathews, Mohammad Saidur Rahman, and Matthew Wright. 2019. Triplet fingerprinting: more practical and portable website fingerprinting with N-shot learning. In ACM CCS 2019. (2019). doi:10.1145/3319535.3354217.

[49] Michael Sonntag. 2019. Malicious DNS trafic in Tor: analysis and countermeasures. In ICISSP.

[50] Michael Sonntag and René Mayrhofer. 2017. Trafic statistics of a high-bandwidth Tor exit node. In ICISSP.

[51] Qixiang Sun, Daniel R. Simon, Yi-Min Wang, Wilf Russell, Venkata N. Padmanabhan, and Lili Qiu. 2002. Statistical identification of encrypted web browsing trafic. In 2002 IEEE Symposium on Security and Privacy. (2002). doi:10.1109/SECPRI.2002.1004359.

[52] Paul F. Syverson, David M. Goldschlag, and Michael G. Reed. 1997. Anonymous connections and onion routing. In 1997 IEEE Symposium on Security and Privacy. doi:10.1109/SECPRI.1997.601314.

[53] 2023. The Tor Metrics Portal. (2023). https://metrics.torproject.org.

[54] 2023. The Tor research safety board. (2023). https://research.torprojec t.org/safetyboard.

[55] Joe Touch, Eliot Lear, Kumiko Ono, Wes Eddy, Brian Trammell, Jana Iyengar, Michael Scharf, Michael Tuexen, Eddie Kohler, and Yoshifumi Nishida. 2023. Service name and transport protocol port number registry. (2023). https://www.iana.org/assignments/service-names-po rt-numbers/service-names-port-numbers.txt.

[56] Tao Wang. 2020. High precision open-world website fingerprinting. In 2020 IEEE Symposium on Security and Privacy. (2020). doi:10.1109 /SP40000.2020.00015.

[57] Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, and Ian Goldberg. 2014. Efective attacks and provable defenses for website fingerprinting. In USENIX Security 2014. (2014).

[58] Tao Wang and Ian Goldberg. 2013. Improved website fingerprinting on Tor. In WPES 2013. doi:10.1145/2517840.2517851.

[59] Tao Wang and Ian Goldberg. 2016. On realistically attacking tor with website fingerprinting. PoPETs, 2016, 4, (2016). doi:10.1515/popets-201 6-0027.

[60] Xiyuan Zhao, Xinhao Deng, Qi Li, Yunpeng Liu, Zhuotao Liu, Kun Sun, and Ke Xu. 2024. Towards fine-grained webpage fingerprinting at scale. In ACM CCS 2024.

## APPENDICES

## A ETHICS

In this section we describe our consideration of ethics as we developed and executed our Tor network measurement plan.

## A.1 Safety

The primary safety guidelines driving our measurement study include collecting only what is adequate, relevant, and necessary for our purpose (data minimization), limiting the granularity of the data that is collected, ensuring security of the measurement infrastructure and confidentiality of the measurement data, and limiting access to measurement infrastructure to a single author.

We took numerous specific precautions to make sure our measurement is as safe as possible. First, our measurement is carried out exclusively by relays under our control, which are identified as part of the same relay family following relay operator best practices. Our measurement is completely passive: it does not alter the default Tor protocol and does not add any load to the network. Second, we use probabilistic sampling to randomly select circuits for measurement. While sampling enables us to limit the total data volume and maintain an accurate, genuine distribution of website access frequency, it also provides plausible deniability for Tor users because any individual circuit that used our relays during measurement is still unlikely to appear in the dataset. Third, we chose to exclude absolute timestamps from the dataset, and we do not precisely specify when the measurement occurred. Precise absolute timing information is not required for WF and there may be some privacy benefit to excluding it. Fourth, we use an irreversible encoding func tion (Eqn. 1) to protect the destination domain name and provide a website label that is consistent within our dataset but whose mapping can no longer be reproduced since the salt was erased. Finally, we encrypt all records using the public part of a public-key encryption scheme before writing to persistent storage or transferring over a network. The secret key is stored ofline to prevent unauthorized decryption.

## A.2 Risks

Our measurement process is designed to be consistent with Tor’s threat model in which exit relays can only observe the destination side of the circuit but cannot link this data to the client side of the circuit. Our measurement data alone cannot be used to identify any individual client.

An adversary could possibly augment our exit-side data patterns with their own client-side flows collected during our measurement period and attempt an end-to-end correlation attack to link a client they observed to a record in our dataset. We mitigated this risk by mapping the true domain name to a random string label using an encoding function that cannot be reproduced or reversed (Eqn. 1), so that a successful correlation attack would still be unable to precisely identify the visited destination. In order to fully deanonymize a flow, the adversary would need to combine the correlation attack with a confirmation attack wherein they link a known labeled flow to a record in our dataset, enabling them to map the random string output of Eqn. 1 to a known label. While not impossible, we believe that such a multi-step attack would be imprecise and thus there is a low risk that it would be successful on a large scale in practice.

## A.3 Benefits

Measurement and publication of our genuine website fingerprinting dataset can help researchers and practitioners improve Tor’s protections against trafic analysis attacks and better quantify the risks that trafic analysis poses to users. Our dataset improves realism relative to synthetic datasets and can help other researchers quickly get started designing WF attacks or defenses without first needing to perform possibly network-invasive measurement themselves. Our dataset also promotes reusability and reproducible research, and may make it more likely that WF defenses developed in research will work well in the real world.

## A.4 Alternatives

One alternative to our measurement approach is to recruit volunteers to opt-in to a measurement study and then only collect patterns on circuits initiated from volunteers. This alternative was rejected because it produces biased samples of trafic at synthetic base rates and it involves human subjects which would add significant additional risk to our study.

## A.5 Board Review

We consulted our organization’s Institutional Review Board (IRB) to determine ifour measurement study required further evaluation as human-subject research. The board determined that our study qualifies as non-human-subject research because we are not directly interacting with subjects nor will the network data we are gathering enable us to identify the people who may be using the network.

We also submitted a document detailing our measurement plans and ethical analysis to the Tor Research Safety Board (TRSB) for review. The review of our initial submission identified several important aspects of our measurement plan that were underspecified, including details around the scope of measurement and our plan for informing stakeholders. Additionally, our submission presented multiple possible methods of dataset release with a request for feedback on the most appropriate. The board expressed preference for a controlled release where the dataset would only be shared with verified researchers upon request. Following an interactive discussion, we extended our measurement plan to include the requested details and plans for a controlled release of the dataset. Following re-review of our updated submission, we received a “No Objections” score and were instructed to move forward with our plans.

## A.6 Community Notification

We notified the Tor community of our plans through a post to the tor-project mailing list [21]. The primary feedback we received was that we should collect more data, which we decided against following the principle of data minimization.

## B SURVEY OF EXISTING WF DATASETS

We surveyed prior work related to website fingerprinting attacks in order to better understand the datasets used to quantify attack efectiveness. We evaluated each dataset among a number of diferent dimensions, as follows.

Year: the time the dataset was collected;

Activity: the kind of user behavior contained in the dataset;   
User model: the way in which users perform the activity;   
Trace generation software: the tools used in activity creation;   
Size: the number of classes and traces in the dataset;   
Availability: the accessibility of the dataset to others;

Attacks: the WF attacks originally evaluated on the dataset. We also noted how each dataset was recorded (that is, the software used and trace observation point, if provided).

The summary of results is shown in Table 3. All datasets surveyed were composed of primarily web activity. Most datasets assume users interact with popular websites, usually those present in the now-discontinued “Alexa Internet” top websites ranking. A few works consider more sophisticated user behaviors: Herrmann et al. [18] collect URLs obtained from monitoring an academic proxy server they had access to; Juárez et al. [29] collect URLs obtained from volunteers browsing the Internet; Panchenko et al. [38] considered URLs obtained from observing Tor HTTP exit trafic, as well as from interacting with popular Internet services such as Twitter and Google; and Deng et al. [13] collected URLs from volunteers browsing the Internet.

The task designated for each dataset may vary. For example, RND-WWW [38], Juárez et al. [29], GDLF-25 [36], GoodEnough [41], BigEnough [33], ALEXA-WSC-FG/BG [34], and

CW/OW [60] are designed to incorporate multiple pages for each of many websites. AWF Recollect [44] and WTT-Time [37] are designed to explore aspects of concept drift. $D S _ { T o r }$ contains .onion sites in addition to ordinary websites. Multi-tab [13, 60] contains only browsing behavior occurring simultaneously in several browser tabs.

All extant datasets are collected synthetically with an automated crawl, often using a single set of software to generate flows (Juárez et al. [29] and Deng et al. [13] both consider the efect that varying versions of Tor Browser Bundle (TBB) may have on attacks). Additionally, nearly every work uses tcpdump to collect packet traces on the client generation ma-<sup>chine.</sup> <sup>Only</sup> <sup>GoodEnough,</sup> <sup>BigEnough,</sup> <sup>and</sup> <sup>�</sup>(<sup>tbs</sup>, <sup>tor</sup>) <sup>[25]</sup> collect cell traces using the tor process directly; GoodEnough and BigEnough are collected at the client position, whereas � tbs<sub>,</sub> tor is collected at the guard position.

Inconsistent purposes, over-simplified user models, and static collection software make it dificult to draw meaningful conclusions about the efectiveness of a WF attack directed at real Tor users. Real Tor clients use a wide variety of software (most network applications supporting SOCKS5 can be used with Tor), interact with non-web services, and do more than just non-interactively fetch random pages on the web. In contrast, GTT23 is the only dataset addressing these weaknesses—it contains traces from real Tor client interacting with real internet services. Moreover, GTT23 is larger than the previous largest dataset by an order of magnitude (AWF $C W _ { g 0 0 }$ [44]) and is larger than most other existing datasets by multiples orders of magnitude; this volume of data is important when training modern deep learning models which may require millions of examples to be efective.

T<sub>a</sub>bl<sub>e</sub> 3 <sub>:</sub> S<sub>ummary o</sub>f <sub>we</sub>b<sub>s</sub>it<sub>e</sub> fi<sub>ngerpr</sub>i<sub>n</sub>ti<sub>ng</sub> d<sub>a</sub>t<sub>ase</sub>t<sub>s cura</sub>t<sub>e</sub>d <sub>over</sub> th<sub>e pas</sub>t 15 <sub>years.</sub> Th<sub>e</sub> <sup>‘</sup>⊥<sup>’</sup> <sub>sym</sub>b<sub>o</sub>l i<sub>s use</sub>d t<sub>o</sub> i<sub>n</sub>di<sub>ca</sub>t<sub>e a</sub> d<sub>a</sub>t<sub>ase</sub>t i<sub>s unname</sub>d <sub>an</sub>d th<sub>e</sub> <sup>‘</sup>-<sup>’</sup> <sub>sym</sub>b<sub>o</sub>l i<sub>s use</sub>d <sub>w</sub>h<sub>en a ce</sub>ll<sup>’</sup><sub>s con</sub>t<sub>en</sub>t<sub>s are</sub> id<sub>en</sub>ti<sub>ca</sub>l t<sub>o</sub> th<sub>e a</sub>b<sub>ove ce</sub>ll Wh<sub>en</sub> th<sub>e year o</sub>f d<sub>a</sub>t<sub>a co</sub>ll<sub>ec</sub>ti<sub>on</sub> i<sub>s no</sub>t <sub>men</sub>ti<sub>one</sub>d <sub>we assume</sub> it i<sub>s aroun</sub>d (<sup>“</sup>ca<sub>.</sub><sup>”</sup>) the associated article<sup>’</sup>s <sub>p</sub>ublication date<sub>.</sub> Not all datasets describe their trace generation software with the same s<sub>p</sub>ecificit<sub>y.</sub> N N<sub>C</sub> N<sub>I</sub> N<sub>B</sub> are th<sub>e</sub> t<sub>o</sub>t<sub>a</sub>l <sub>num</sub>b<sub>er o</sub>f t<sub>races</sub> i<sub>n</sub> th<sub>e</sub> d<sub>a</sub>t<sub>ase</sub>t th<sub>e num</sub>b<sub>er o</sub>f <sub>pos</sub>iti<sub>ve c</sub>l<sub>asses</sub> th<sub>e num</sub>b<sub>er o</sub>f i<sub>ns</sub>t<sub>ances per pos</sub>iti<sub>ve c</sub>l<sub>ass an</sub>d th<sub>e num</sub>b<sub>er o</sub>f b<sub>ac</sub>k<sub>groun</sub>d t<sub>races.</sub> Th<sub>e</sub> <sup>“</sup>Att<sub>ac</sub>k<sub>s</sub><sup>”</sup> <sub>co</sub>l<sub>umn s</sub>h<sub>ows a</sub> li<sub>s</sub>t <sub>o</sub>f WF <sub>a</sub>tt<sub>ac</sub>k <sub>papers eva</sub>l<sub>ua</sub>t<sub>e</sub>d <sub>on</sub> th<sub>e</sub> d<sub>a</sub>t<sub>ase</sub>t<sub>.</sub>
<table><tr><td rowspan="2">Ref. Name</td><td rowspan="2"></td><td rowspan="2">Year Activity Activity Detailed</td><td rowspan="2"></td><td rowspan="2"></td><td rowspan="2">User Model</td><td rowspan="2">Trace Gen. Software</td><td rowspan="2">N</td><td rowspan="2">NC</td><td rowspan="2">NI NBg</td><td rowspan="2">Available</td><td rowspan="2">Attacks</td></tr><tr><td>Links from real-world academic</td></tr><tr><td></td><td>[18] ⊥ (Hermann)</td><td>2008</td><td>Web</td><td>proxy server</td><td>Index page</td><td>Autofox</td><td>8.5×103</td><td>775</td><td>≈10</td><td>Dead link</td><td>[18]</td></tr><tr><td>[9]</td><td>⊥(Cai)</td><td>Ca.2012</td><td>Web</td><td>Alexa top sites</td><td>Index page</td><td>tor 0.2.1/2</td><td>3.2×104</td><td>800</td><td>≈40</td><td>No</td><td>[9]</td></tr><tr><td></td><td>[58] levdata2</td><td>Ca.2013</td><td>Web</td><td>Alexa top sites Popular blocked sites, Alexa top</td><td>Index page</td><td>tor 0.2.4.7; TBB 2.4.7</td><td>4 ×103</td><td>100</td><td>40</td><td>Online</td><td>[38,58]</td></tr><tr><td></td><td>levdata3</td><td></td><td>sites</td><td></td><td></td><td>TBB 3.5.1;</td><td>9×102</td><td>4</td><td>10 8.6×102</td><td></td><td></td></tr><tr><td>[57] k-NN</td><td></td><td>Ca.2014</td><td>Web</td><td>Sensitive sites, Alexa top sites</td><td>Index page Index page,</td><td>iMacros 8.6.0 TBB (2/3.X);</td><td>1.4×104</td><td>100</td><td>90 5 ×103</td><td>Online</td><td>[1, 37, 38, 48,57-59]</td></tr><tr><td></td><td>[29]⊥(Juárez)</td><td>Ca.2014</td><td>Web</td><td>Alexa top sites, volunteer browsing</td><td>visited pages</td><td>Selenium</td><td>4.3×104</td><td>200</td><td>≈40 3.5×104</td><td>On request</td><td>[29]</td></tr><tr><td></td><td>[59]⊥(Wang)</td><td>2014</td><td>Web</td><td>Sensitive sites, Alexa top sites Twitter, Alexa one-click, Google</td><td>Index page Random</td><td>tor 0.3.6.4; TBB 3.6.4 9 ×103 TBB 3.6.1;</td><td></td><td>100</td><td>40 5 ×103</td><td>No</td><td>[59]</td></tr><tr><td></td><td>[38] RND-WWW</td><td>Ca.2016</td><td>Web sites</td><td>Trends, Google Random, censored</td><td>subpage</td><td>Chickenfoot; iMacros; Scriptish</td><td>1.6×105 1,125</td><td></td><td>40 1.2×105</td><td>Dead link</td><td>[38]</td></tr><tr><td></td><td>TOR-Exit</td><td></td><td></td><td>HTTP requests of real Tor users</td><td>Visited page Index page,</td><td></td><td>2.1×105</td><td></td><td>2.1×105</td><td></td><td></td></tr><tr><td></td><td>WEBSITES</td><td></td><td></td><td>Popular websites</td><td>random subpage</td><td></td><td>5.3×103</td><td>50 105</td><td></td><td></td><td></td></tr><tr><td>[17] DSTor</td><td></td><td>Ca.2016</td><td>Web</td><td>Alexa top sites, popular .onion sites Index page</td><td></td><td>TBB; Selenium tor 0.2.8.11; TBB 6.5;</td><td>1.1×105</td><td>85</td><td>≈90 1 ×105</td><td>Dead link</td><td>[17,37]</td></tr><tr><td></td><td>[44] AWF CW900</td><td>2017</td><td>Web</td><td>Alexa top sites</td><td>Index page</td><td>Selenium</td><td>2.3×106</td><td>9002,500</td><td></td><td>Online</td><td>[5, 36, 37,</td></tr><tr><td></td><td>AWF Recollect</td><td></td><td></td><td></td><td></td><td></td><td>1 ×105</td><td>200</td><td>500</td><td></td><td>44,48]</td></tr><tr><td></td><td>AWF Open</td><td></td><td></td><td></td><td></td><td></td><td>8 ×105</td><td></td><td>200 2,000 4 ×105</td><td></td><td></td></tr><tr><td>[47] DF</td><td></td><td>Ca.2018</td><td>Web</td><td>Alexa top sites</td><td>Index page</td><td>tor-browser- selenium</td><td>1.4×105</td><td></td><td>95 1,000 4.1×104</td><td>Online</td><td>[36, 43, 47,48]</td></tr><tr><td></td><td>[37] WTT-time</td><td>2018</td><td>Web</td><td>Alexa top sites</td><td>Index page</td><td>tor 0.4.0.8; tor-browser-crawler</td><td>8 ×104</td><td>100</td><td>300 5 ×104</td><td>On request</td><td>[37]</td></tr><tr><td>[41]</td><td>Good Enough</td><td>2020</td><td>Web</td><td>Alexa top pages, random subpage</td><td>Index page</td><td>TBB 9.0.2</td><td>2 ×104</td><td>500</td><td>20 1 ×104</td><td>Online</td><td></td></tr><tr><td>[56]</td><td>⊥ (Wang)</td><td>2019</td><td>Web</td><td>Alexa top sites</td><td>Index page Random</td><td>tor 0.4.0.1; TBB 8.5a7</td><td>1 ×105</td><td>100</td><td>200 8 ×104</td><td>Partially Online</td><td>[56]</td></tr><tr><td></td><td>Wikipedia</td><td></td><td></td><td>Wikipedia browsing</td><td>subpage</td><td></td><td>2 ×104</td><td>100</td><td>100 1 ×104</td><td></td><td></td></tr><tr><td></td><td>[36] GDLF-25</td><td>Ca.2021</td><td>Web</td><td>Alexa top sites</td><td>Random subpage</td><td>tor-browser-crawler 9.4×104 2,400</td><td></td><td></td><td>39</td><td>On request</td><td>[36]</td></tr><tr><td></td><td>GDLF-OW</td><td></td><td></td><td>Links from Rimmer et al. [44]</td><td>Random subpage</td><td></td><td>7 ×104</td><td></td><td>7 ×104</td><td></td><td></td></tr><tr><td></td><td>[33] BigEnough</td><td>2021</td><td>Web</td><td>Open PageRank top pages</td><td>Index page Index page</td><td>TBB</td><td>3.8×104</td><td>950</td><td>20 1.9×104</td><td>On request</td><td></td></tr><tr><td></td><td>[13] Multi-tab</td><td>2022</td><td>Web</td><td>Alexa top pages</td><td>(multi-tab) Random</td><td>TBB; Selenium tor-browser-</td><td>5.7×105</td><td></td><td></td><td>Online</td><td>[13]</td></tr><tr><td></td><td>[25] D(tbs, tor)</td><td>2022</td><td>Web</td><td>Wikipedia browsing Popular websites, links from</td><td>subpage</td><td>selenium TBB 11.0.10;</td><td>2 ×104</td><td>98</td><td>200</td><td>Online</td><td></td></tr><tr><td></td><td>[4] Drift</td><td>Ca.2023</td><td>Web</td><td>Rimmer et al. [44]</td><td>Index page Visited</td><td>tor-browser- selenium 0.6.3</td><td>1.5×104</td><td></td><td>90 ≈110 5 ×103</td><td>Online</td><td>[4]</td></tr><tr><td></td><td>GTT23</td><td>2023</td><td>Any</td><td>Real Tor usage</td><td>service Random</td><td>Real client software</td><td>1.4×107</td><td></td><td>〈 1.1 × 10⁶ domains 〉</td><td>On request</td><td></td></tr><tr><td></td><td></td><td>[34] ALEXA-WSC-FG/BG Ca. 2024</td><td>Web</td><td>Alexa top sites, random subpage</td><td>subpage Random</td><td>TBB 7.5.6</td><td>8.6×105</td><td>9,000</td><td>90 4.5×104</td><td>No</td><td>[34]</td></tr><tr><td>[60] CW/OW</td><td></td><td>Ca.2024</td><td>Web</td><td>Alexa top sites, random subpage</td><td>subpage (multi-tab)</td><td>TBB</td><td>8.1×104 1,000</td><td></td><td>109.3×103</td><td>Online</td><td>[60]</td></tr><tr><td>[46] D1-D7</td><td></td><td>2024</td><td>Web</td><td>Tranco top sites</td><td>Index page</td><td>TBB 10.5; Chrome 112.0</td><td>7.4×105</td><td>100</td><td>700 4.00×103</td><td>Online</td><td>[46]</td></tr></table>