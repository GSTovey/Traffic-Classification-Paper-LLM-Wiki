# SaTor: Exploring Satellite Routing in Tor to Reduce Latency

Haozhi Li<sup>∗</sup>

School of Cyberspace Science and Technology

Beijing Institute of Technology

Email: lihaozhi@bit.edu.cn

Tariq Elahi School of Informatics University of Edinburgh Email: t.elahi@ed.ac.uk

Abstract—High latency is a critical limitation within the Tor network that has a negative impact on web application responsiveness. A key factor exacerbating Tor latency is the creation of lengthy circuits that span across geographically distant regions, causing significant transmission delays. A common solution involves modifying Tor’s circuit-building process to reduce the likelihood of selecting lengthy circuits. However, this strategy compromises Tor’s routing randomness, increasing the risk of deanonymization. Reducing Tor’s latency while minimizing security degradation presents a challenge.

This paper proposes and investigates SaTor, a satelliteassisted routing scheme to reduce Tor latency. By equipping Tor relays with satellite network access, SaTor could accelerate slow circuits via satellite transmission, without biasing the existing path selection process. Our performance evaluation, using a simulator we developed along with real-world measurements, shows that over the long term, SaTor provides an expected speed-up of 21.8 ms for over 40% of circuits, with only 100 top relays equipped with satellite service. Our research uncovers a viable way to overcome Tor’s latency bottleneck, serving as a practical reference for its future enhancement.

## 1. Introduction

Tor is a popular tool for anonymous communication, protecting millions [1] of users against surveillance [2]. Currently, the Tor network is supported by thousands of volunteer relays. The popularity of Tor, a boon for online privacy, places considerable demand on network performance. Improving the network quality of service (QoS) to improve user experience is an important research topic within Tor community [3], [4], [5], [6], [7], [8].

Measuring the time taken for traffic traveling from one endpoint to another, latency has a direct impact on user experience, especially for interactive applications such as web browsing and online calling [9]. However, Tor often experiences higher latency than regular Internet [1], [10]. A key reason is that Tor traffic is often routed through a series of geographically distributed relays. A Tor client accessing a server may construct a short, fast circuit with all intermediate relays in close proximity, or a longer, slower path spanning the globe. This routing mechanism, while essential for Tor’s anonymity, extends the data’s journey and results in high latency [3], [8], [11].

Prior work on reducing Tor latency looks at avoiding slow paths, by preferring relays that are geographically close or have historically demonstrated favorable latency performance [3], [4], [6], [7], [11], [12]. However, these methods may compromise Tor’s anonymity, as they undermine the randomness of circuit path, making traffic routes predictable to adversaries [13], [14], [15], [16]. An alternative approach, ShorTor [8], incorporates extra via relays into conventional three-hop circuits, allowing the newly configured circuits to be faster than the standard ones. While ShorTor avoids altering Tor’s default path selection, its strategy of recruiting extra relays per circuit still introduces security risks and increases network workload. Currently, it remains an open challenge to reduce Tor’s latency without substantially compromising security or increasing network overhead.

Satellite communication, as a rapidly developing and deployed technology, provides stable and cost-effective network services to millions. The rise of satellite networks has driven research into their performance advantages and novel applications. Some studies suggest that satellite routing may offer faster transmission than terrestrial fiber owing to its higher signal propagation speed. Theoretically, satellite traffic travels at the speed of light in a vacuum via spot-beams, while terrestrial traffic may reach at most two-thirds of the speed of light in an optical fiber due to a physical limit [17]. Consider two relays communicating with each other either via terrestrial Internet or a satellite orbiting in lowearth orbit (LEO, 550 kilometers) above the earth’s surface. Disregarding node processing delays, the pure propagation latency of satellite traffic becomes lower than that of terrestrial paths when the distance between endpoints exceeds ≈1,100 kilometers, as the higher signal speed offsets the longer physical path [18], [19], [20].

Another latency advantage of satellite routing lies in its simpler structure, where traffic is relayed through only a few satellites. By contrast, traffic in terrestrial routing often traverses multiple network domains controlled by various service providers, leading to unnecessarily long paths and a greater likelihood of congestion [21], [22], [23]. The advantages of satellite routing illuminate a plausible insight to overcoming Tor’s latency challenges: by using satellite transmissions between some relays—during the times when terrestrial network is slow—while adhering to Tor’s default path selection, it is possible to reduce latency without using extra relays in circuits or biasing circuit path. This paper presents an exploratory study on the latency of satelliteassisted Tor (SaTor for short), aiming to answer:

Could the introduction of satellite routing technology reduce latency in the Tor network? If so, in what specific ways could Tor take this benefit?

Answering this question requires comparing satellite and terrestrial routing latencies between all pairs of Tor relays, a challenging task due to the impracticality of equipping every relay with satellite connectivity for direct latency measurements. As a solution, we developed a simulator which could estimate latency between any pair of Tor relays at any given time via both satellite and terrestrial routing. The simulator tracks real-time satellite coordinates, identifies reachable routing paths between relay pairs, and calculates routing latency by dividing the physical path length by a probabilistic distribution of traffic speeds. The speed distribution is derived from public datasets of satellite and terrestrial latencies, specifically LENS [24] and RIPE [25]. Compared to existing satellite routing simulations [26], [27], [28], which use a constant speed of light for all latency calculations, our simulator captures both temporal and geographical characteristics in latency.

To calibrate potential simulation errors and assess the latency benefits of satellite routing in actual Tor connections, we conducted real-world latency measurements on a subset of relay pairs using a dual-homed testbed with access to both satellite and terrestrial services. The measurements spanned more than a month, characterizing the long-term latency gap between satellite and terrestrial routing. We then compared these measured latencies with the simulated results on the same subset of relay pairs and derived an error distribution to calibrate subsequent simulations.

Both the simulation and measurement show that, while satellite routing may not outperform terrestrial links under normal conditions, more than half of relay pairs achieve notable reductions at tail-percentile (>90th) latencies, with improvements averaging up to 1.4 seconds (≈ 50% lower than terrestrial latency). Since tail latencies significantly affect end-user experience [29], SaTor presents substantial potential for performance improvement. To this end, we propose a latency reduction scheme for SaTor which supposes a subset of relays to be equipped with satellite network services, enabling traffic to use satellite paths when terrestrial routes are slow. This involves relays installing a satellite dish (similar to a home Wi-Fi) and subscribing to a satellite provider, such as Starlink [30]. These dual-homed relays actively measure latency to other relays through both their satellite and terrestrial interfaces, and instruct Tor to route traffic through the faster interface by adaptively modifying the routing table in the operating system. This process, operating within the system’s network stack, requires no modifications to the existing Tor system.

The evaluation of dual-homed SaTor shows that, in a best-case scenario where all relays have satellite access, RTT latency is reduced by an average of 21.7 ms (36.6%) across all relay pairs and 41.4 ms (41.0%) across all circuits over a long-term period, with even greater gains at tail latencies. In a more realistic setup with only 100 high-bandwidth relays using satellite, SaTor still accelerates over 40% of circuits, achieving an average RTT reduction of 21.8 ms, translating to ≈400 ms faster page load times for users. Regarding SaTor’s practicality, based on our investigation, over 94% of Tor relays are in regions with current or upcoming satellite service. While ≈70% of relays are cloud-hosted and depend on provider support for satellite access—an area where some providers are already progressing [31], [32]—the remaining 30% of non-cloud relays are sufficient to realize a substantial portion of SaTor’s potential. With only a moderate share of relays adopting satellite access, SaTor is unlikely to increase an adversary’s network visibility compared to vanilla Tor.

Our contributions are summarized as follows:

We propose the idea of integrating satellite routing into Tor, exploring a novel application of satellite networks and offering a fresh perspective on addressing Tor’s long-standing latency challenges.

We present SaTor Simulator, a tool for evaluating real-time satellite and terrestrial latencies. Using globally measured datasets of satellite and terrestrial networks, we assess latency in the current Tor. We also release our simulator publicly<sup>1</sup>.

We measured real-world terrestrial and satellite latencies in Tor to validate the advantages of satellite routing and refine the SaTor simulator.

We propose a practical scheme for deploying satellite routing functionality in Tor and conduct a comprehensive feasibility assessment from both costbenefit and security perspectives.

## 2. Background

## 2.1. The Tor Network

2.1.1. Onion Routing. As a key technique in Tor, onion routing encapsulates messages in multiple layers of encryption, and transmits them through a “circuit” containing a series of relays [2], [33]. Each relay decrypts a single layer to uncover the next message destination. This technique maintains the anonymity between communication endpoints, as each intermediary knows only the identity of the immediately preceding and following nodes.

A typical Tor circuit contains three relays, each selected from a large set of volunteer-operated hosts. The first relay, known as the entry guard, is chosen from a list of trustworthy and stable nodes, serving as the entry point for the client’s data to the Tor network. The last relay, known as the exit relay, is responsible for connecting Tor to the public Internet. The middle relay connects the entry guard to the exit to further obscure the source of the traffic.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/3d10085208b215d96f7110f7fcd55d9d5c7cadc26bac82a4516d3648a3ed5c99.jpg)  
Figure 1: Overview of satellite communications.

2.1.2. Tor Latency Reduction. The end-to-end latency of a Tor circuit $\mathcal { L } _ { \mathrm { c i r } }$ arises from two sources: intra-relay processing and inter-relay transmission, expressed as follows:

$$
\mathcal {L} _ {\mathrm{cir}} = \mathcal {L} _ {\mathrm{guard}} ^ {\mathrm{P}} + \mathcal {L} _ {\mathrm{middle}} ^ {\mathrm{P}} + \mathcal {L} _ {\mathrm{exit}} ^ {\mathrm{P}} + \mathcal {L} _ {\mathrm{g} \rightarrow \mathrm{m}} ^ {\mathrm{T}} + \mathcal {L} _ {\mathrm{m} \rightarrow \mathrm{e}} ^ {\mathrm{T}}\tag{1}
$$

where $\mathcal { L } _ { \mathrm { X } } ^ { \mathrm { P } }$ is the processing latency within relay X, and $\mathcal { L } _ { \mathrm { X  Y } } ^ { \mathrm { T } }$ means the transmission latency during the route from relay X to Y. This expression excludes latency components external to the Tor network, such as those incurred between client and guard, and between exit and the destination server.

To reduce the intra-relay processing latency, Tor maintains minimal hardware requirements for relays and uses a bandwidth-weighted algorithm for load balancing across relays. Further efforts may focus on optimizing the Tor software and enhancing its traffic management mechanism [34], [35], thereby reducing processing delays within relays. Moreover, the rapid growth in the number of relays can also contribute to reducing Tor’s intra-relay latency.

High inter-relay transmission latency is a crucial factor that hampers Tor’s performance, which is the primary focus of this paper. Such latency is closely tied to the routes of circuits. By default, Tor selects circuit routes based solely on relay bandwidth and certain security constraints [36]. This often results in slow circuits over distant geographical or heavily congested areas. A common solution involves modifying Tor’s path selection algorithm to reduce the likelihood of choosing distant or congested relays in a single circuit [3], [4], [34]. However, this strategy introduces a degree of predictability into which circuits the users are likely to use, which can be exploited to narrow down the anonymity set of users, facilitating more targeted attacks for de-anonymization [37], [38], [39]. To address this challenge, this paper explores satellite routing as a potential gamechanger for reducing latency in the Tor network.

## 2.2. Satellite Communication

Utilizing orbiting satellites to relay signals, satellite communication technology provides a way for achieving low-latency transmission. This technology has advanced notably in recent years, with an emphasis on deploying vast constellations of small, low Earth orbit (LEO) satellites to provide global, high-speed internet connectivity.

2.2.1. Routing Traffic via Satellite. The principle of satellite data routing is illustrated in Fig. 1. As shown by the solid black line, user data is transmitted from a home dish to a nearby satellite and relayed down to a ground station, forming a “bent-pipe” link structure. The data is then routed via a Point of Presence (PoP) to destination server. For the reverse path, the server’s data is sent via the PoP to the ground station, and then to the user via satellite connection. This single bent-pipe routing strategy is the most fundamental approach in most satellite constellations.

Satellite routing strategies are rapidly evolving. According to Starlink’s filings, inter-satellite links (ISLs), which are laser-based connections between satellites, are being incorporated into their satellites [40]. With ISLs, traffic can be relayed through multiple satellites before being transmitted to a ground station near the destination. This ISL-enabled routing retains most of the transmission path in space, where signals can, in theory, propagate at the speed of light. As a result, it offers lower latency compared to the single bentpipe method, in which a large portion of the transmission still relies on terrestrial links.

2.2.2. Commercial LEO Satellite Constellation. Situated at an altitude ranging from 500 to 2,000 kilometers, LEO satellites enable much lower communication latency compared to traditional geostationary satellites. However, the coverage of a single LEO satellite is limited, so large satellite groups must be arranged in a constellation for reliable and performant global coverage.

SpaceX’s Starlink is currently the largest low Earth orbit (LEO) satellite constellation. As of May 2025, SpaceX has launched over 8,000 satellites into orbits approximately 550 kilometers above Earth, providing service to millions of users [41], [42]. SpaceX plans to expand the Starlink constellation to as many as 34,000 satellites in the future. Eutelsat’s OneWeb is another major LEO constellation, with 660 satellites launched to an altitude of approximately 1,200 kilometers [43]. Other initiatives, including Kuiper, Yinhe, and Telesat, also have ambitious deployment plans underway. The rapid advancement of commercial LEO constellations signals a promising future for satellite-based Internet, offering potential solutions to the persistent challenges faced by conventional network applications.

2.2.3. Latency Reduction using Satellite Routing. The latency $\mathcal { L } _ { \mathrm { X  Y } } ^ { \mathrm { T } }$ from relay X to relay Y, say the path traverses n intermediate devices $\{ d _ { 1 } , d _ { 2 } , \dots , d _ { n } \}$ , is modeled as:

$$
\mathcal {L} _ {\mathrm{X} \rightarrow \mathrm{Y}} ^ {\mathrm{T}} = \mathcal {L} _ {\mathrm{X} \rightarrow \mathrm{d} _ {1}} ^ {\mathrm{T}} + \sum_ {i = 1} ^ {n} \mathcal {L} _ {d _ {i}} ^ {\mathrm{P}} + \sum_ {i = 1} ^ {n - 1} \mathcal {L} _ {d _ {i} \rightarrow d _ {i + 1}} ^ {\mathrm{T}} + \mathcal {L} _ {\mathrm{d} _ {\mathrm{n}} \rightarrow \mathrm{Y}} ^ {\mathrm{T}}\tag{2}
$$

where $\mathcal { L } _ { d _ { i } } ^ { \mathrm { P } }$ denotes the processing latency at device $d _ { i } ,$ such as queuing delay in a router, and $\mathcal { L } _ { d _ { i } \to d _ { i + 1 } } ^ { \mathrm { T } }$ represents the transmission delay between devices $d _ { i }$ and $d _ { i + 1 }$

Compared to traditional terrestrial routing, satellite routing offers the potential to reduce both transmission latency $\begin{array} { r } { { \underset { \displaystyle \mathcal { L } ^ { \mathrm { T } } } { \mathrm { m g } } } } \end{array}$ and processing latency $\mathcal { L } ^ { \mathrm { P } }$ . Transmission latency can be estimated as the ratio of total link length to signal propagation speed. As illustrated in Fig. 1, satellite routing relays traffic through only a few satellites before reaching a ground station near the destination. In contrast, terrestrial routing often involves complex paths across multiple network domains and devices, leading to longer travel distances and increased processing delays. Additionally, due to the physical properties of the transmission medium (satellite beam in vacuum versus optical signal in fiber), satellite traffic can theoretically propagate at the speed of light, while terrestrial traffic is limited to about two-thirds of that speed. Therefore, prior studies suggested that satellite routing would outperform terrestrial routing, particularly in long-distance transmissions [18], [19], [20], [44].

In addition to the above theoretical analyses, researchers have conducted both simulative and empirical evaluations of satellite routing latency [26], [27], [28], [45], [46], [47]. These studies demonstrate that satellite routing generally offers latency performance comparable to that of terrestrial routing at the current stage, and even lower latency for transmissions between certain regions. They also indicate that factors such as unstable weather conditions, satellite link reconfiguration, sub-optimal routing path, and the sparse distribution of ground stations can hinder satellite routing from realizing its full potential. However, to the best of our knowledge, no existing work has investigated the potential latency benefits and practical integration strategies of satellite routing in the context of Tor. This gap serves as the primary motivation for our work.

## 3. SaTor Latency Evaluation Methodology

## 3.1. Evaluation Goals

This paper aims to explore the potential latency reduction achieved by integrating satellite routing technology into the existing Tor. This evaluation requires estimating both satellite and terrestrial transmission latencies across all Tor relays over an extended period. The evaluation should be scalable across the entire Tor network and flexible enough to accommodate rapidly expanding satellite constellations, including both current developmental stages and future deployments. We conducted both programmatic simulation and real-world measurements, as introduced below.

## 3.2. Evaluation Material

The data and knowledge in evaluation include:

Tor Circuits. A Tor circuit contains two hops across three relays: entry, middle and exit. We collected a dataset containing 100,000 Tor circuits using an instrumented Tor client. The client constructs circuits using a single consensus file at 00:00 AM on December 24, 2024. These circuits include ≈ 120,000 unique hops (relay pairs) across 6,964 relays. Our goal is to evaluate the latencies of all circuits in this dataset to assess the latency performance of the entire Tor. Since SaTor focuses exclusively on the latency between relay pairs, the circuits do not include the connections between client and entries, nor between exits and servers.

Satellite Constellation. A constellation consists of satellites, ground stations, and PoPs (Fig. 1). Satellite movements are described by two-line-element (TLE) files—a standard format for recording the trajectory of earth-orbiting objects. The North American Aerospace Defense Command (NO-RAD) regularly releases the TLE files of LEO constellations, allowing for tracking real-time satellite coordinates (latitude, longitude) [48]. The coordinates of ground stations and PoPs are available on websites managed by astronomy enthusiasts [49], [50]. While these sites are unofficial, their accuracy is satisfactory for scientific research [26], [27], [28]. The evaluation is performed on Starlink constellation in December 2024, which consists of over 6,700 operational satellites, 25 PoPs, and 277 ground stations.

Baseline Latency. We collect satellite and terrestrial latency measurements from public datasets as an evaluation baseline. The satellite latencies are from LENS dataset [24], which measures the ICMP RTTs between global-distributed Starlink dishes and PoPs. The LENS data we collected spans a two-month period from April to May, 2024, a total 1.624 billion data points across five geographical locations. The terrestrial latencies are sourced from RIPE Atlas, a global network to measure Internet performance [25]. We extract over 104.64 million ICMP RTT latencies from RIPE dataset, covering a one-week period starting on Sep. 2, 2024. Full data information is in Table 4 and 5, Appendix A.

GeoIP. The geographical coordinates of each Tor relay are determined based on their IPs using GeoIP service, thus estimating the length of traffic route. The GoeIP service sources information from MaxMind dataset [51], which claims 79% and 72% of IPs are within a 100km error-range in Germany and the US, respectively, where the majority of Tor relays are located. The coordinates of RIPE probes are provided in RIPE’s official website, deemed accurate.

## 3.3. Evaluation Approach

The evaluation begins with measuring satellite and terrestrial latency across a subset of Tor circuits using a realworld testbed. Next, we simulated the latencies for the same subset over a custom-built simulator, using the gap between simulation and measurement to improve its accuracy. Finally, the calibrated simulator was employed to estimate the latency of Tor circuits that could not be directly measured.

3.3.1. Real-world Measurement in Tor. As shown in Fig. 2, two Tor clients, controlled by Stem [52], run in separate Docker containers within a dual-homed host, binding to the satellite interface and the terrestrial interface, respectively. Two Tor relays, denoted as $\mathrm { R } ^ { m }$ and R<sup>e</sup>, along with an echo server program, run on another host. The client host is in Waterloo, Canada, and the server host is in Los Angeles, US. The two clients, using their bound interfaces, continuously transmit probe packets to the echo server through different circuits $c _ { i } = \{ \mathrm { R } ^ { g _ { i } } , \mathrm { R } ^ { m } , \mathrm { R } ^ { e } \}$ , where the entry $\mathrm { R } ^ { g _ { i } }$ is sequentially rotated from the Tor consensus. Such measurement constructs numerous circuits that originate from Waterloo, traverse diverse relays worldwide as entries, and terminate in the US. Note that Stem can build circuits with designated entries, not limited to Guard-flagged relays.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/39e156df85048033ec4ae2dc0f587e552bca82a7e96bd5f9d8e073e2946686da.jpg)  
Figure 2: SaTor evaluation over real-world Tor connections.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/e76f40c7ae713e85dd87af1cb956ef0e8cdf0d9f2ea641a0f6aad051c4ab6260.jpg)  
Figure 3: Procedures of simulative evaluation on SaTor.

The echo server responds immediately upon receiving each probe packet, enabling RTT calculations at the clients. Packet loss would trigger retransmissions, producing high RTTs. This RTT consists of the latency from the client to $\mathrm { R } ^ { g _ { i } }$ (via either satellite or terrestrial network) and from $\mathrm { R } ^ { g _ { i } }$ to $\mathrm { R } ^ { m }$ (via terrestrial network), assuming negligible latency from $\mathrm { R } ^ { m }$ to $\mathrm { R } ^ { e }$ . Comparing the RTTs from the two clients yields an assessment of satellite versus terrestrial latency in Tor, since with the same entry $\operatorname { R } ^ { g _ { i } }$ , the $\mathrm { R } ^ { g _ { i } }  \mathrm { R } ^ { m }$ segment is identical and the observed difference isolates the satellite benefits on the path from client to R<sup>gi</sup>.

3.3.2. Programmatic Simulation. We developed a simulator to estimate the satellite and terrestrial latency between each Tor relay pair at any given time. The core concept for calculating latency is to divide the physical length of the traffic route, which is determined using the geographical coordinates of endpoints, by the estimated propagation speeds of traffic. This concept is used in popular satellite routing simulators, such as Hypatia [28] and StarPerf [26]. As shown in Fig. 3, the simulator operates in five procedures:

1. Traffic Speed Approximation. The simulator approximates the probability distribution of satellite and terrestrial traffic speeds based on baseline latencies as follows:

1) Calculate the traffic speeds as the ratio of the geographical round-trip length to the RTT latencies.

2) Partition the range between the maximum and minimum speeds using n delimiters $\delta _ { 1 } , \ldots , \delta _ { n }$

3) For each delimiter $\delta _ { i } ,$ , let $f _ { i }$ denote the proportion of speed values lower than $\delta _ { i }$ . The collection $\{ \delta _ { i } \mapsto f _ { i } \}$ therefore defines an Empirical Cumulative Distribution Function (ECDF).

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/3099dece769c044f7e8b8b4750eedd47a7eb635f8860d48752012bbb7a3cd07f.jpg)  
Figure 4: Satellite routing topology to estimate traffic speed.

4) To yield a speed sample, draw a random number $u \sim \mathcal { U } ( 0 , 1 )$ and select the delimiter $\delta _ { i }$ such that $f _ { i }$ is the closest cumulative frequency to u. The selected $\delta _ { i }$ is then taken as the sampled speed.

For terrestrial traffic, the geographical round-trip length is estimated by doubling the great-circle distance between RIPE Atlas probes, computed using their coordinates obtained from the official Atlas website, which are considered accurate. Note that this estimation accounts only for the great-circle distance (i.e., the shortest path along the Earth’s surface) between probe pairs and does not consider actual routing detours through intermediate devices such as routers and switches. Since terrestrial traffic speed may depend on geographic distance, we partitioned probe pairs into groups of 1,000 km intervals. For each group, a separate traffic speed distribution was computed for latency simulation.

For satellite traffic, the round-trip length is estimated based on satellite routing topology. The LENS latency data are obtained by pinging Starlink’s PoPs from multiple client terminals. The traffic path can be represented as:

Client ←→ Satellite ←→ Ground Station ←→ PoP,

with the segment “Client ↔ Ground Station” carried over satellite links and “Ground Station $ \mathrm { P o P } ^ { \prime \prime }$ over terrestrial links. As shown in Fig. 4, the satellite path length is:

$$
S _ {\mathrm{len}} \approx 4 \cdot \sqrt {\left(\frac {d _ {c g}}{2}\right) ^ {2} + h ^ {2}},
$$

where h ≈ 550 km is the orbit altitude of LEO satellites, and $d _ { c g }$ is the great-circle distance between the client and the ground station. Since the ground stations and PoPs are often geographically close $( d _ { g p } \ll d _ { c g } )$ with an RTT of $\approx 5$ ms [47], the satellite traffic speed is given by:

$$
S _ {\mathrm{speed}} \approx \frac {S _ {\mathrm{len}}}{r t t _ {i}}
$$

where $r t t _ { i }$ is an RTT sampled from the dataset. Note that each rtt includes the $\approx 5$ ms ground-station-to-PoP latency, leading to an underestimation of satellite traffic speed and a conservative estimate of satellite latency reduction.

2. Tor Circuit Collection. Circuits are collected using an instrumented Tor client. Stem library [52] is used to send signals to the client, continuously instructing it to construct new circuits. The client is instrumented so that once a circuit is selected and saved, the relevant function will immediately return without actually building the connection. In this way, the simulator can quickly gather a large number of circuits based on up-to-date consensus file, ensuring no impact on the Tor network’s burden. Moreover, it fully leverages the most recent algorithms in the Tor system, offering an advantage over classical but outdated circuit generation tools like TorPS [53]. Although the circuits are collected from a single client, given that Tor’s path selection relies on the same consensus and algorithm globally, our dataset is representative of worldwide conditions for Tor.

3. Public Data Collection. The TLE files for satellite constellations, along with the coordinates of ground stations and PoPs, are sourced from public websites. The TLE files are acquired from NORAD website [48], while the coordinates of ground stations and PoPs are taken from the KML file downloaded from Google Maps [49].

4. Routing Graph Generation. The simulator maintains a routing graph for the entire Tor network. Each node in the graph represents a communication entity, including a relay, satellite, ground station, or PoP. Note that intermediate devices along terrestrial links, such as routers and switches, are not included. Each graph edge represents a data link, with its weight corresponding to the latency between the two connected entities. This latency is estimated using the physical distance between peers and a traffic speed sampled from the distribution obtained in Procedure 1, depending on whether the link is terrestrial (groundstation-to-PoP, PoP-to-relay) or over satellite (relay-to-satellite, satellite-togroundstation). For terrestrial links, traffic speed is sampled from the distribution within the link’s distance interval.

At regular intervals, the simulator updates the routing graph, recalculating the coordinates of each satellite and the physical distance among nodes. It then adjusts the edge weights by resampling a speed for each link to recalculate its latency. The simulator is flexible to simulate various routing strategies of satellite constellation by switching the availability of each type of links, detailed in Appendix B.

5. Latency Calculation. Using the routing graph, the latency between two relays is estimated by summing the weight of each reachable path connecting them. The simulator is designed to output the top-K shortest paths utilizing an efficient algorithm [54]. Given that Starlink may not always route traffic through the shortest path, the simulator estimates satellite routing latencies by averaging the top-K paths. The evaluation uses K = 10 as the baseline, while also examining how varying K affects satellite latency.

3.3.3. Simulation Calibration. The simulation is based on latencies measured from global locations over an extended period, which encompass both the transmission latency over terrestrial fiber or satellite links, and the processing latency within intermediate satellites, ground stations, and routers. Continuously sampling from these latencies, our simulation replicates both spatial and temporal variability in satellite and terrestrial transmission. Compared to prior satellite routing simulators [26], [27], [28], which assume the speed of light for satellite links and two-thirds of the speed of light for terrestrial links, SaTor simulator offers higher fidelity.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/cb8e2d1ef5952fa26adfec1205f10070260ec7a8d740c5f555a2537a74845da4.jpg)  
Figure 5: An illustration of circuit in SaTor.

However, simulation errors may arise due to the different latency characteristics between ICMP and TCP. LENS and RIPE latency measurements, relying on ICMP, may not capture Tor’s TCP-based latency with multi-layer encapsulation. For example, in ICMP measurements, a lost packet leads to a timeout with no latency recorded, whereas in TCP a lost packet triggers retransmission, resulting in high delay. Unfortunately, to the best of our knowledge, no large-scale TCP-based latency dataset for satellite networks is publicly available. To calibrate protocol-level simulation errors, the relative differences between the simulated and measured latencies are computed over the same circuit path using the same interface, deriving an error distribution. The subsequent simulation is adjusted using error rates sampled repeatedly from this distribution, with the mean of the adjusted values providing a final latency estimate.

## 4. SaTor Latency Reduction Scheme

A further question is: If satellite routing can outperform terrestrial routing in latency between certain relays at specific times (it can, as we will show in Section 5), how can Tor take this benefit? A naive idea is to entirely switch certain links from terrestrial to satellite routing. However, while this may reduce latency at certain times, it could increase it at others, yielding sub-optimal gains. This section presents a latency reduction scheme for SaTor, featuring adaptive dualhoming routing based on active latency measurements.

## 4.1. Overview

SaTor proposes equipping a subset of Tor relays with satellite network services in addition to their existing terrestrial connections. These dual-homed relays then communicate with other relays via satellite interfaces during periods when terrestrial routing is slow. As shown in Fig. 5, a Tor client accesses a server through three relays that are selected using Tor’s default algorithm. The middle relay chooses to route traffic through satellite network to reach the exit, as it is considered faster than terrestrial link during that period. Thereby, with the circuit path remaining unchanged, SaTor could achieve lower latency compared to the current Tor. This design requires additional hardware and software to be integrated into Tor, as detailed below.

## 4.2. SaTor Hardware Configuration

SaTor assumes that certain Tor relays install a satellite dish and subscribe to a satellite network provider, similar to purchasing a Wi-Fi router and subscribing to traditional Internet service. The new satellite interface creates a dualhoming configuration alongside the existing terrestrial interface. Relays can then route traffic to other relays through the faster interface based on real-time latency performance.

Starlink, the most widely used satellite network, offers a business plan that includes a public IP address and a personal plan that provides only a private IP [30]. A Tor relay requires a public IP to be uploaded to Tor consensus for handling inbound connections from other relays, but a private IP is sufficient for outbound connections. Therefore, SaTor can choose either plan from Starlink, provided that at least one public IP is available on either the terrestrial or satellite interface. Fig. 6 illustrates a configuration where relay SaTorRelay1 operates a terrestrial interface (eth0, with public IP 129.97.7.84) and a satellite interface (eth1, with private IP 192.168.1.139). SaTorRelay1 publishes its public address by setting the ‘ORPort’ and ‘Address’ fields in Tor’s configuration file, allowing inbound connections from other relays to reach eth0. When establishing outbound connections to other relays, SaTorRelay1 can select between eth0 and eth1 for optimal latency performance. This functionality is achieved by modifying the routing table in the operating system, without requiring changes to Tor software.

If SaTorRelay1 subscribes to Starlink’s business plan, obtaining a public IP for both satellite and terrestrial interfaces, it could upload both IPs to Tor consensus for inbound connections, similar to running two relays on a single physical host. This would allow relays without satellite access to benefit from satellite acceleration by connecting to the satellite IP of SaTorRelay1. However, it would require modifying Tor’s default relay selection, as some relays with satellite IPs may have to be prioritized to achieve such acceleration. Therefore, SaTor adopts the “one inbound, two outbound” configuration, as shown in Fig. 6. All changes occur after Tor’s current path selection, and relays choose fast interface solely for establishing outbound connections to the next relay. Moreover, to prevent end-to-end traffic correlation by satellite network provider, SaTor operates exclusively within the Tor network, meaning that Tor clients and exit relays do not conduct SaTor’s functionality.

## 4.3. SaTor Software Functionality

SaTor works as an independent program separate from the Tor system. As shown in Fig. 6, in SaTorRelay1, SaTor process periodically measures latency to a set of other relays through both satellite and terrestrial interfaces, maintaining a table of the measured latencies. Latency can be measured using hping3 tool [55], by attempting to establish TCP connections to an open port of relays, as recorded in Tor’s consensus. Based on the measured latencies, the SaTor process updates the routing table in operating system, connecting to some relays via the satellite interface, and others via the terrestrial. As a result, the Tor relay software, operating at the application layer, will establish new connections using the network interface specified by the system’s routing table, without requiring any code changes.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/e80dd5fb50cbe2b40ad118d04421620b60d34acbb90adc28a0e97bf8d30a011d.jpg)  
Figure 6: Routing architecture between a dual-homing SaTor relay with the remaining of Tor network.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 SaTor Latency Measuring
1: Define data structures:
2:    relay_list: List of all Tor relays
3:    latency_history[relay]: Historical records of the satellite and terrestrial latencies for each relay
4:    last_time[relay]: Last measurement time for relays
5:    priority[relay]: Measurement priority for relays
6: Function GetFasterIfaceEN (relay):
7:    $p_{sat}, p_{ter} \leftarrow$ Probability of satellite/terrestrial interface being faster in latency_history[relay]
8:    return $-(p_{sat} \log_2 p_{sat} + p_{ter} \log_2 p_{ter})$ // Entropy
9: Function UpdatePriority(time_now, a):
10:    for each relay ∈ relay_list:
11:    $H_r \leftarrow$ GetFasterIfaceEN (relay)
12:    $F_r \leftarrow$ time_now - last_time[relay]
13:    priority[relay] ← a · $H_r + (1 - a) \cdot F_r$
14:    end for
15: Function MeasureLatency (relay):
16:    $t_{sat} \leftarrow$ Measured satellite latency to relay
17:    $t_{ter} \leftarrow$ Measured terrestrial latency to relay
18:    latency_history[relay].append($t_{sat}, t_{ter}$)
19: Function MainLoop(T, N, a):
// T: interval time to pause before next measurement
// N: Maximum of relays to be measured each time
// a: Tunable, for calculating relay measurement priority
20:    while True:
21:    time_now ← Get current time
22:    UpdatePriority(time_now, a)
23:    top_relays ← Select top n relays by priority
24:    for each relay ∈ top_relays:
25:    MeasureLatency (relay)
26:    last_time[relay] ← time_now
27:    end for
28:    sleep(t)
</div>

SaTor’s latency measurement, as outlined in Algorithm

<table><tr><td colspan="4">SaTor Latency Table</td><td colspan="2">Routing Table in OS</td></tr><tr><td>Relay IP</td><td>Last Time</td><td>Latency Record</td><td>Measure Priority</td><td>Use Ter.</td><td> $IP_i$  dev eth0 src 129.97.7.84 $IP_j$  dev eth0 src 129.97.7.84...</td></tr><tr><td> $IP_i$ </td><td> $T_i$ </td><td> $t_{sat}^i > t_{ter}^i$ </td><td>0.8</td><td rowspan="3">Use Sat.</td><td rowspan="3"> $IP_k$  dev eth1 src 192.168.1.139 $IP_l$  dev eth1 src 192.168.1.139...</td></tr><tr><td> $IP_k$ </td><td> $T_k$ </td><td> $t_{sat}^k < t_{ter}^k$ </td><td>0.1</td></tr><tr><td>-</td><td>-</td><td>-</td><td>-</td></tr></table>

Figure 7: SaTor maintains a latency Table to record the measured latencies, and updates the system routing table to control relay’s routing behavior for reducing latency.

1, is conducted at regular intervals $T$ and measures up to N relays each time. Relays are prioritized for measurement based on a score calculated by the time since the last measurement and the uncertainty of the faster interface to them. This uncertainty is quantified as the entropy of the random variable for each interface being faster, based on historical records. Simply put, if the terrestrial interface is highly likely to be faster than satellite for reaching a relay, it is continuously used for communication to that relay without the need for frequent measurements. After each interval T, SaTor updates the priority scores, selects the top N relays with the highest priority, and sends probe packets through both interfaces to measure latency. Subsequently, SaTor updates its latency table and the system’s routing table, as shown in Fig. 7. Until the next measurement cycle, Tor follows the routing table for connecting to other relays. Adjusting T and N could balance SaTor’s efficiency and effectiveness, as well as the extra workload imposed on Tor.

## 5. SaTor Evaluation Result

## 5.1. Setup Overview

The simulation was conducted on 100k Tor circuits (over 120k relay pairs), as described in Section 3.2. Each relay pair was simulated every 5 minutes over a 24-hour period, covering multiple LEO satellite orbits (≈100 minutes each) [19] to capture the periodic latency variations of satellite routing. The simulation adopted ISL-enabled routing strategy (Fig. 16(d)), as currently used in Starlink. The SaTor latency measurement, as introduced in Section 3.3, encompasses 7,280 circuits with distinct entry relays, conducted over ≈30 rounds during August 2024. In each round, every circuit is measured 10 times at 1-second intervals. Ultimately, 6,897 circuits yielded over 300 valid latency data points on both satellite and terrestrial interfaces, which were selected to comprise the measurement dataset.

The evaluation employs various percentiles of the latency data. For each relay pair, we obtain a simulated set and a measured set, each containing ≈300 data points. The 50th percentile of these latencies reflects link performance under typical conditions, indicating that latency is lower than this value half of the time and higher the other half. Values above the 95th percentile indicate performance under congested scenarios, and the 90th percentile represents the latency experienced by the majority of users [56].

The evaluation is organized as follows. First, baseline traffic speeds are analyzed to offer a preliminary view of satellite and terrestrial latencies. Second, simulation and measurement are compared to derive an error distribution to correct subsequent simulations. Third, corrected simulations are performed across all circuits. Fourth, a dual-homing scenario, as proposed in Section 4, is simulated to evaluate SaTor’s best-case potential. Finally, several practical challenges in SaTor deployment are investigated.

## 5.2. Baseline Traffic Speed

The ECDFs for the speed of satellite and terrestrial traffic are derived from LENS and RIPE datasets. Satellite traffic speed is calculated along actual routing paths, from the testbed, through satellites to a ground station. Terrestrial speeds are estimated using straight-line distances between RIPE probes, due to the difficulty of predicting real-world Internet routing paths, as introduced in Section 3.3.

As shown in Fig. 15 (Appendix A), when the distance between endpoints is 0-2k kilometers (0-4k km round-trip), satellite traffic often transmits faster than terrestrial traffic. Beyond this range, terrestrial routing generally achieves higher speeds, while satellites still retain a non-negligible chance of being faster. This is likely due to the fact that longhaul terrestrial links often follow optimized backbone routes, while short paths may suffer from inefficient inter-domain routing, leading to higher-than-necessary delays [21], [22]. However, the higher speed of satellite traffic does not necessarily equate to lower latency, since the routing path is often longer due to bent-pipe detours via satellites and ground stations. Satellite routing yields a latency advantage only when the speed gain outweighs the additional path length, which will be examined by SaTor simulator.

## 5.3. Simulation Error Evaluation

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/337f4d0c3f883a17caa91785c912c22aaa63dc39944578efa7ef2c33be1ad958.jpg)  
(a) Satellite (Starlink)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/bf66ef14adeec88a7b992b8332803b8719aa40a86517ca19a4e5dac51a5bae05.jpg)  
(b) Terrestrial  
Figure 8: Relative error between simulated and measured latencies across Waterloo circuits at varying percentiles.

The traffic speed CDF enables latency estimation between two relays using their geographical distance. However, the ICMP speeds may deviate from Tor’s TCP-based, onion-routed traffic. For a given circuit, let n simulated latencies be $\mathcal { L } _ { s } = \{ l _ { s } ^ { 1 } , l _ { s } ^ { 2 } , \ldots , \overline { { { \ O } } } l _ { s } ^ { n } \}$ and n measured latencies be $\mathcal { L } _ { m } ~ = ~ \{ l _ { m } ^ { 1 } , l _ { m } ^ { 2 } , . ~ . ~ . , l _ { m } ^ { n } \}$ . The simulation-measurement relative error at the i-th percentile is calculated as $e _ { i } ~ =$ $( P _ { i } ( \mathcal { L } _ { m } ) - P _ { i } ( \mathcal { L } _ { s } ) ) / P _ { i } ( \mathcal { L } _ { m } )$ , where $P _ { i } ( \cdot )$ denotes the operation that extracts the i-th percentile from a latency set. We examine 5,280 circuits with both simulated and measured data. Some circuits are excluded because their relays either exited the network or changed fingerprints during the time gap between the simulation and measurement.

Fig. 8 shows the relative errors between simulated and measured latencies. The x-axis is the evaluated latency percentiles, and the y-axis displays the relative error in percentage. The dashed line shows the median error across all circuits, while the shaded regions indicate error ranges. For instance, the lightest shaded band represents the range between the 5th and 95th percentile of errors across circuits. As shown in Fig. 8(a), satellite simulations generally exhibit high fidelity. Below the 70th percentile, 90% of circuits show relative errors between ≈-10% and 25%. Beyond the 75th, the error range widens, reaching from -30% to 60% at the 95th. A further trend is that beyond the 95th many circuits show positive errors, indicating that simulations underestimate latency compared to real measurements.

As shown in Fig. 8(b), below the 50th percentile, terrestrial simulations yield a narrow error range of roughly -15% to 40% for 90% of circuits. At the 75th, this 90% error range shifts to between -40% and 15%, while beyond the 90th, it further broadens to -90% to 70%. Across all percentiles, over 50% of circuits stay within an error range between roughly -45% to 60%, supporting the overall effectiveness of simulation. Another notable trend is that the simulation tends to overestimate real-world measurements between the 50th and 95th latency percentiles, but underestimates them beyond the 95th percentile. Such underestimation is likely because tail latency reflects packet loss and retransmission in TCP, which ICMP-based simulations cannot capture.

Tail latency typically indicates link congestion with increased variability and unpredictability, leading to higher simulation errors. Terrestrial simulation exhibits higher error levels than satellite routing, mainly due to its coarsegrained approach, which estimates latency using straightline distances and overlooks actual circuitous routing paths. In contrast, the satellite simulation tracks the precise coordinates of intermediate nodes to replicate fine-grained routing paths. Simulation discrepancies may also arise from the gap between the globally collected latency dataset and the specific latency characteristics at the measurement testbed. To mitigate this, the simulator is calibrated using the observed errors before being applied to the entire Tor network.

## 5.4. Simulation Error Calibration

At each latency percentile i, the relative errors between simulation and measurement across all circuits form a distribution $\mathcal { E } _ { i } .$ . Then, the simulator estimates the i-th percentile latency by sampling $\mathcal { E } _ { i }$ for R times $( R = 1 0 \mathrm { k }$ in the following evaluation) to adjust the baseline simulation, yielding R latency candidates. The mean of these candidates is taken as the representative estimate, while the 5th and 95th percentiles of them define a 90% confidence interval (CI).

Fig. 9 shows the CDFs of the calibrated simulation and measurement for the 50th, 90th, and 95th latency percentiles. The solid line represents the measured data, the dashed line indicates the representative latency estimate, and the shaded area denotes the 90% simulation CI. At the 50th percentile (Fig. 9(a) and 9(d)), the representative estimate matches the measurement. At the 90th percentile, the satellite simulation still demonstrates high fidelity (Fig. 9(b)), whereas the terrestrial simulation exhibits slight underestimation, as some simulated latencies fall below the measured values (Fig. 9(e)). This trend becomes more pronounced at the 95th percentile (Fig. 9(c) and 9(f)). Nevertheless, in all cases, the 90% CI encompasses the actual measurement curve.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/3257965df223b59c1e76f0b766b53e1b6c6910fe2529b0e5e0d9db88405ceb7f.jpg)  
(a) Sat. $P _ { 5 0 }$

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/428f9247429110ee74eb4df34ee2031bf3db3cf2a7550fe32c2a4ac558e856a1.jpg)  
(b) Sat. $P _ { 9 0 }$

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/eb22d5e46e6ba6ff154133176dca1b4d6c255ee3a71f1cace408aad3a33db7fc.jpg)  
(c) Sat. $P _ { 9 5 }$

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/9be98f0daf393187c7ea5324a10fd87437e96dc2134526c52b6ac12a6b6d8c9b.jpg)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/08d729ffac93de9e6e8d917ad4cca95b1114359d8809efd178d3ea2a2eed8cc2.jpg)  
(d) Ter. $P _ { 5 0 }$  
(e) Ter. $P _ { 9 0 }$

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/b6edbe14ca61f7f3714bf9801714278cf4824b8c0eccc4ffdcbc5116c72a403d.jpg)  
(f) Ter. $P _ { 9 5 }$  
Figure 9: Latency CDFs from corrected simulations and real measurements for Waterloo-originating circuits.

Calibration Limitations. Overall, simulation calibration consists of three steps. First, the testbed measures TCPbased latencies in real Tor on a subset of circuits, each comprising two segments: the client–entry segment, which traverses either satellite or terrestrial links, and the entry–middle segment, which always traverses terrestrial links. Second, the simulator reproduces these circuit paths and settings to generate ICMP-based latency simulations. Third, an error distribution is derived by comparing the simulated and measured results to calibrate subsequent simulations. However, such calibration settings have two limitations.

First, the measurements do not directly capture the latency of individual relay pairs but instead reflect circuitlevel latency over two consecutive pairs. The measured satellite latencies are also biased, as the entry–middle segments always traverse terrestrial networks. These issues may introduce skew when the calibration is applied to pairlevel latency simulations. This limitation arises because the satellite testbed is research-oriented and does not permit running public proxy services such as Tor relays. With only Tor clients deployable, prior relay-pair-level latency measurement tools such as Ting [57] cannot be used.

Second, while the operation of repeated sampling and averaging can capture overall error trends across circuits, it may smooth out deviations at the individual level, making calibration less effective for circuits whose errors deviate significantly from the average, especially for tail latencies with greater variability and a wider error range.

TABLE 1: Simulated and Measured Latency Reduction After Using Satellite Routing for Waterloo-originating Circuits

<table><tr><td rowspan="2">Percentile</td><td colspan="6">Relative Reduction (%)</td><td rowspan="2">Avg. Reduction</td></tr><tr><td>&lt;20</td><td>20–40</td><td>40–60</td><td>60–80</td><td>80–100</td><td>Sum. &gt;20</td></tr><tr><td>50th</td><td>100.00% (99.89)1</td><td>0.00% (0.03)</td><td>0.00% (0.04)</td><td>0.00% (0.04)</td><td>0.00% (0.00)</td><td>0.00% (0.11)</td><td>0.00% (48.95)</td></tr><tr><td>90th</td><td>97.06% (79.72)</td><td>2.35% (5.88)</td><td>0.00% (4.12)</td><td>0.00% (5.90)</td><td>0.59% (4.38)</td><td>2.37% (20.28)</td><td>25.06% (57.89)2</td></tr><tr><td>95th</td><td>19.01% (39.30)</td><td>71.38% (10.96)</td><td>8.55% (18.84)</td><td>0.47% (24.94)</td><td>0.59% (5.96)</td><td>80.65% (60.70)</td><td>29.93% (58.08)</td></tr></table>

<sup>1</sup> Indicating that for the 50th-percentile latency over the simulation period, 99.41% of circuits show $< 2 0 \%$ reduction after using satellite, while the corresponding fraction in real measurements is 99.89%.  
<sup>2</sup> Among relay pairs with significant latency reduction (> 20%), satellite routing is, on average, 25.06% faster than terrestrial routing in simulation; the corresponding figure from real measurements is 57.89%.

Despite these limitations, recall that the calibration targets two goals. The first is to capture protocol-level differences between ICMP and TCP latencies, which the current setup could capture. The second is to assess the benefits of satellite routing relative to terrestrial routing. This assessment remains valid as long as the latency benefits of satellite routing are not overestimated, regardless of moderate errors in their individual estimates. Table 1 presents the relative reduction between satellite latency $( l _ { \mathrm { s a t } } )$ and terrestrial latency $( l _ { \mathrm { t e r } } )$ , computed as $( l _ { \mathrm { t e r } } - l _ { \mathrm { s a t } } ) / \dot { l } _ { \mathrm { t e r } } \times 1 0 0 \%$ based on both measurement and calibrated simulation. Blue text indicates underestimation by the calibrated simulation (more circuits actually experience such level of reduction), while red indicates overestimation.

At the 50th percentile, the measurement shows that 0.11% of circuits achieve a significant reduction (>20%), whereas the simulation reports none. At the 95th, the simulation overestimates this figure at 80.65%, compared to the measured 60.70%. However, this overestimation only occurs in the 20–40% reduction range, as the simulation underestimates the number of circuits achieving larger reductions. Overall, the calibrated simulator is expected to conservatively estimate satellite latency reduction, providing cautious assertions regarding the benefits of satellite routing.

## 5.5. Satellite and Terrestrial Latency in Tor

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/03e0f8236c3438caf895aaeac2f2a6bec9a41603afd2d08ca505bfa7f74e6161.jpg)  
(a) Sat. $P _ { 9 0 }$

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/38482666cce3314f00a49b739fe05a94bb91bab06bbe917182b1389f84c31bf1.jpg)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/ee4dbf48966272ce0545a6610c4cd9d1094be3181c3465d5a1073296bff1a017.jpg)  
(b) Sat. P<sub>95</sub>

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/9c6031886ce60f5c464a3ef24c52cb14389a0f0661c7a9c9b3763a9be819a83a.jpg)  
(c) Sat. P<sub>98</sub>

(d) Ter. $P _ { 9 0 }$  
![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/798a8c047f750f8fedfeb587792b7504ea7eddf8df5a58d6bc7b3607481b0e25.jpg)  
(e) Ter. $P _ { 9 5 }$

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/896e7974891b087be33e7df39541320f5cc53bed5561245e777d845f332381cf.jpg)  
(f) Ter. P<sub>98</sub>  
Figure 10: Simulated latency histogram for pairs using satellite (a-c) and terrestrial routing (d-f).

Fig. 10 presents the latency histograms for all 120k relay pairs, focusing exclusively on tail latencies at the

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/ae60c4198f9aa30f2a12d4f20abd46258c1afd0b6f1b4438a80955b195e6801e.jpg)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/44a8745caabfe61ddcf7857d4d35d86eb5ab37685d34d14b99bb4eb8248eb836.jpg)  
(a) Lat-Varied Pairs (%)  
(b) Variation (ms)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/e17ccd954d2616d2daaa56eba364493dfb3aa1db6e4e3478e6e8c8903bf7b0cf.jpg)  
(c) Variation (%)  
Figure 11: Simulated latency variation using satellite routing across the 1-99th percentile throughout simulation.

90th, 95th, and 98th percentiles, as satellite routing shows limited latency reduction at lower percentiles in the measurements. At the 90th percentile, satellite routing shows similar latency distributions as terrestrial. At the 95th, satellite routing achieves latency reduction efficacy, presenting a slightly smaller portion of slow relay pairs compared to terrestrial. At the 98th percentile, its effectiveness becomes pronounced, eliminating all tail pairs with latencies >1k ms.

TABLE 2: Simulated Latency Reduction of Satellite Routing

<table><tr><td rowspan="2">P</td><td colspan="6">Relative Reduction (%)</td><td rowspan="2">Avg.</td></tr><tr><td>&lt;20</td><td>20–40</td><td>40–60</td><td>60–80</td><td>80–100</td><td>&gt;20</td></tr><tr><td>90th</td><td>99.47%</td><td>0.53%</td><td>0.00%</td><td>0.00%</td><td>0.00%</td><td>0.53%</td><td>24.39%</td></tr><tr><td>95th</td><td>81.95%</td><td>13.28%</td><td>4.48%</td><td>0.29%</td><td>0.00%</td><td>18.06%</td><td>34.26%</td></tr><tr><td>98th</td><td>69.66%</td><td>10.84%</td><td>9.62%</td><td>8.10%</td><td>1.78%</td><td>30.35%</td><td>49.85%</td></tr></table>

Table 2 presents the percentage relative latency reduction of satellite routing compared to terrestrial routing. At the 90th percentile, approximately 0.53% of relay pairs show significant reductions (>20%), with an average reduction of 24.39%. This share increases to 18.06% at the 95th and 30.35% at the 98th. Fig. 11 illustrates the overall latency reduction of satellite routing across 1-99th percentiles. Satellite routing begins to show notable latency reduction above the 90th percentile, and at the 99th, it accelerates over 55% of relay pairs by an average of 1.4s (or 50%). However, it is worth noting that a comparable portion of relay pairs (≈45% at the 99th) experience no latency reduction, and in fact suffer from an average latency increase of nearly 3x when switching from terrestrial to satellite routing, as shown by the red line in Fig. 11.

Impact of Sub-optimal Satellite Routing. Prior studies suggest that satellite networks may not always route traffic along the shortest path [47], [58], so the satellite simulations above report the average latency of the top K = 10 shortest routes. To examine the impact of different K values, we resimulated satellite latencies for all 100k circuits over a onehour testing period, using K values up to 200. Compared to K = 10, the average satellite latency across all circuits increases by 4.56% for K = 50, 7.24% for K = 100, and 10.68% for K = 200. Nonetheless, even with K = 10, the simulation tends to underestimate the benefits of satellite routing compared to real measurements, as reported in Table 1. The community is actively refining routing algorithms in satellite networks, which will make latency converge toward the shortest paths [58], [59]. Therefore, choosing K = 10 is a reasonable basis for simulation.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/6d255b209ecae10e569298b733fb262ce02328c6703028c6e2ffe9defa2de90a.jpg)  
(a) Latency-Varied Pairs (%)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/176dda43edf4ebd16e5403a5c345a4ff3d0c1b419e4ae20747abd726e4959cc1.jpg)  
(b) Latency-Varied Circuits (%)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/5169f913649b674f496dd8ca2265a87dc7866bfeb502fbb051ea6d3a8fcd21ed.jpg)  
(c) Latency Variation (ms)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/646bbc9eefef6436683a4b1b530efb43a8004ab14f7be5b651cfb8821c0ae7d6.jpg)  
(d) Latency Variation (%)

Figure 12: Simulated latency in dual-homed SaTor, including the percentage of pairs (a) and circuits (b) experiencing latency reduction, and the average latency reduction or increment in milliseconds (c) and percentage (d).  
![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/6bd4cc19a1920ecfdf71ec9229ef9cdb5bfbeb0b9c1cec3ecc1e8988f6ec11a2.jpg)  
(a) Reduced Circuits (%)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/363d72e0c2320cfcd011c0fbd7e14d8fdf38c46fc1c333f43bae6ac63a3516c9.jpg)  
(b) Ave. Reduction (ms)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/147ac347ded7157b11efd6f56782b9276c042904dc26bd28be9545883672cf60.jpg)  
(c) Ave. Reduction (%)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/b432ff21f81c8a71aabf16adc9f6cbd5537d4fa76dfe986e586c816f9dbeed18.jpg)  
(d) Ave. Reduction CDF (ms) (e) Ave. Reduction CDF (%)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/89cdcc3d585995e44e98b1421c5470907b78dafbc3edcc2d46426a50b43f3509.jpg)  
Figure 13: Circuit latency reduction averaged across all percentiles of dual-homed SaTor in the three deployment scenarios.

TABLE 3: Concurrent Tail Latency Probability Between Dual-Terrestrial and Satellite–Terrestrial Links

<table><tr><td rowspan="2">Measurement Source</td><td colspan="11">Country of Destination Relays</td></tr><tr><td>Germany</td><td>Japan</td><td>New Zealand</td><td>Singapore</td><td>Brazil</td><td>Australia</td><td>UAE</td><td>US</td><td>Canada</td><td>Indonesia</td><td>Argentina</td></tr><tr><td>London (Dual Terrestrial)</td><td>2.81%</td><td>6.38%</td><td>8.80%</td><td>18.05%</td><td>6.25%</td><td>4.07%</td><td>17.78%</td><td>3.57%</td><td>7.40%</td><td>15.07%</td><td>25.63%</td></tr><tr><td>Waterloo (Sat. and Ter.)</td><td>6.62%</td><td>4.01%</td><td>5.83%</td><td>5.38%</td><td>5.23%</td><td>5.50%</td><td>6.67%</td><td>40.80%</td><td>49.76%</td><td>/</td><td>/</td></tr></table>

Values denote the conditional probability that the second link is above the 95th percentile latency, given that the first link is also above this threshold.

## 5.6. Dual-Homing Latency in SaTor

The preceding evaluation confirms SaTor’s latency advantages, particularly in tail latencies that critically impact user experience. The dual-homing scheme proposed in Section 4 suggests equipping relays with satellite access alongside their existing terrestrial connectivity, enabling real-time interface switching for latency optimization. The evaluation begins by envisioning an ideal scenario in which all relays are dual-homed, providing a best-case estimate.

software periodically probes latency to 50 other relays at 5- minute intervals. It is found that nearly all links exhibit latency reduction at tail percentiles (Fig. 12(a) and Fig. 12(b)). This aligns with expectations, as the relay can keep selecting the faster interface throughout the simulation. Combined with the results in Fig. 12(c) and Fig. 12(d), at the 99th percentile, over 98% of pairs show an expected latency reduction of over ≈1.2 seconds (82%), with almost all circuits showing ≈2.8 seconds (87.9%). Using the average across all percentiles as a metric, SaTor scheme achieves an expected latency reduction of ≈21.7 ms (36.6%) at relay pair level and ≈41.4 ms (41.0%) at circuit level.

Fig. 12 presents the overall latency reduction achieved by integrating the dual-homing routing scheme in SaTor, at both relay-pair and circuit levels. In this setup, the SaTor

## 5.7. Incremental Deployment of SaTor

Equipping all relays with satellite service, as assumed in the previous evaluation, is a costly endeavor. This subsection evaluates whether SaTor’s dual-homing scheme, deployed only to a small subset of relays, can still deliver meaningful benefits. The evaluation considers three deployment scenarios: top-n, weighted-n, and random-n. The top-n scenario assumes that the n relays with the highest likelihood of being selected adopt satellite connectivity, achieving the highest efficacy with minimal investment. The weighted-n assumes that relays adopt satellite with a probability proportional to their normalized bandwidth—higher-bandwidth relays have a greater incentive and resources to invest in SaTor. This scenario differs from the top-n in that satellite adoption is probabilistic rather than deterministic. In the random-n scenario, relays adopt satellite independently at random.

As shown in Fig. 13(a)–13(c), in the top-n scenario, equipping just 50 relays with SaTor accelerates over 99.3% of circuits, achieving an expected latency reduction of ≈21.9 ms (22.4%). This reduction is based on the average latency across all percentiles. Expanding to top 1k relays yields an expected reduction of ≈33.9 ms (34.3%) across all circuits. In the weighted-n scenario, ≈50 SaTor relays achieve an expected reduction of ≈21.2 ms (21.4%) for 37.3% of circuits, while 1k relays benefit 82.5% of circuits with an average of 27.5 ms (27.8%). The random-n shows the least efficacy: with 1k SaTor relays, only 35.2% of circuits are accelerated with an average of 22.6 ms (22.1%).

Fig. 13(d) shows the CDF of absolute latency reduction across all circuits under the weighted-n scenario—the most reasonable assumption in practice. With 100 SaTor relays, ≈24% of circuits show a latency reduction greater than 10 ms, 3.95% exceed 50 ms, and 0.07% exceed 100 ms. When using 600 SaTor relays, 44.5% of circuits show a reduction greater than 10 ms, 9.1% exceed 50 ms, and 1.2% exceed 100 ms. In terms of relative reduction (Fig. 13(e)), deploying 600 SaTor relays yields a >10% latency reduction for 47.2% of circuits, >25% for 29.9%, and >50% for 10.1%.

Practical Impact on User Experience. The evaluation uses RTT latency, which may not directly reflect SaTor’s benefits from an end-user perspective. Based on [8], a 50 ms RTT reduction roughly corresponds to a 1 second (≈20x) page-load-time (PLT) improvement during web browsing. With 100 SaTor relays in the weighted-n scenario, ≈40.5% of circuits see an average RTT reduction of 21.8 ms, translating to an expected ≈400 ms PLT minimization. Also, 3.95% of circuits see >50 ms RTT reduction and 0.7% exceed 100 ms, implying >1 s and >2 s PLT improvements, respectively. Notably, these figures are averaged across all percentiles. SaTor’s impact at tail latencies, those most affecting user experience, would be more significant.

## 5.8. Practicality of SaTor

SaTor requires the financial investment for equipping relays with satellite service, and the extra bandwidth required for real-time latency measurements. Currently, satellite networks are widely deployed by several commercial companies, providing services to millions with comparable cost to traditional terrestrial networks. For example, Starlink offers a minimum monthly subscription fee of 80 USD [42], while fiber subscriptions may range from 50 to 100 USD per month [60]. With Starlink’s rapid expansion, satellite costs are expected to decrease further. Regarding additional bandwidth costs, assuming each SaTor relay sends a probe packet via both satellite and terrestrial interfaces to 50 other relays every 5 minutes, the total bandwidth consumption is roughly 3MB per relay per day, a minimal overhead compared to Tor’s recommended relay bandwidth [61].

Currently, over 94% of relays are located in regions where Starlink service is available. Based on the Tor metrics [1] and the IPinfo database [62], cloud platforms host ≈70% of relays, followed by general ISPs (20%), business (3%), and education networks (7%), as discussed in Appendix D. While deploying SaTor on cloud-hosted relays may require collaboration with cloud providers, major cloud companies are partnering with satellite services, making SaTor deployment hopeful [31], [32]. On non-cloud relays (30% of all relays), direct access to physical machines makes satellite installation simpler. In the weighted-n setting, equipping 50 non-cloud relays accelerates 14.5% of circuits with an average of 22.8 ms, and removing the non-cloud constraint increases these figures to 37.3% and 21.2 ms, respectively.

The adoption of the SaTor may require additional configurations, such as installing satellite dishes (similar to home Wi-Fi). While this may present challenges for resourceconstrained relay operators, several factors encourage its practicality. First, ≈20% of top relays are hosted by universities and companies that can afford, or already operate, satellite terminals. Each terminal can serve multiple relays, making pilot SaTor deployment feasible [63]. Second, Tor allocates most of its budget to program services, indicating the capacity to support infrastructure improvements [64]. Third, SaTor can achieve full functionality without requiring any changes to the Tor application itself, while assistance from non-profit organizations may help relay volunteers overcome deployment and configuration challenges [65].

## 5.9. Broader Dual-homing Spectrums

Dual-homing schemes can be extended to broader spectrums, i.e., dual terrestrial links from different providers. However, dual-homing effectiveness depends on the independence of latency variations between the two links. If both links go slow under similar congestion, benefits are limited. To assess this, we evaluate latency correlations across different types of dual-homed links under two scenarios.

First, we deploy two virtual private servers in London, each hosted by a distinct cloud provider. The two servers simultaneously probe global Tor relays using hping3 [55], recording RTTs for roughly one day per relay. Second, we analyze measurements from the dual-homed Waterloo testbed, which comprises one satellite and one terrestrial link. In this setup, traffic originates from Waterloo, traverses global relays as entries, and terminates in Los Angeles. In these measurements, the geographic location of each destination relay is identified only at the country level. Tail latency correlation between the two links is quantified as the conditional probability that one link experiences tail latency (above the 95th percentile) given that the other also does.

As shown in Table 3, dual-terrestrial links from London exhibit strong tail-latency correlation toward Singapore, the UAE, Indonesia, and Argentina, with conditional probabili ties >15%, whereas other destinations show moderate correlation. This reflects the routing topology of the terrestrial Internet. When destinations are close, network connectivity is often rich, allowing traffic from different providers to traverse largely disjoint paths. For distant destinations, especially those far from the global Internet core, dual-terrestrial routes often converge at the same exchange points or transit backbones. Congestion at these shared bottlenecks can lead to simultaneous latency spikes across both links, as observed in prior studies [66], [67]. Exceptions exist, however, such as on Europe-US routes, where correlation remains low despite long distances, likely due to multiple high-capacity submarine cables and extensive exchange infrastructure.

Dual-homed satellite–terrestrial links (the second row of Table 3) exhibit weaker tail-latency correlation than dualterrestrial links in most cases. Note that the measurements in the Waterloo testbed are circuit-level, where the dual-homed links share a terrestrial hop from the entry relay to the fixed endpoint in the US. Thus, the observed correlation reflects (i) the relationship between the satellite and terrestrial paths on the client–entry segment, and (ii) the inherent correlation of the common terrestrial segment from entry to destination. Even with this overlap, the overall correlation remains low, supporting the view that satellite and terrestrial paths behave largely independently in most cases.

An exception arises when the entry relays are located in the US or Canada, which exhibit a conditional probability >40%. Two factors may account for this. First, in these cases, the circuit length is short, so processing delays within relays and the testbed become more significant. Second, in satellite routing, when endpoint distance is small, the proportion of the path that traverses satellite links from the client to the PoP decreases (Fig. 1). Once traffic reaches the PoP, the remaining route becomes terrestrial, leading to strong latency correlation between the two links. In contrast, for distant destinations, a large fraction of the path traverses inter-satellite links, and traffic rejoins the terrestrial Internet only near the endpoint. This results in orthogonal paths to terrestrial ones, keeping latency correlation low.

Overall, SaTor’s satellite–terrestrial dual-homing fits Tor. From a cost perspective, satellite and terrestrial network services are now comparable, and satellite costs are expected to decline further. In terms of performance, the satellite–terrestrial combination offers greater benefits for distant transmissions, aligning with Tor’s characteristic of building cross-country circuits to maintain anonymity. While dual-terrestrial links may benefit short hops, these alreadyfast connections are not major latency bottlenecks, where single-homing is often enough. We further find that satellite acceleration tends to be pronounced for pairs with geographic distances between 5–6k km, detailed in Appendix C. Operating on an independent physical layer, satellite routing is a compelling complement to terrestrial links in Tor.

## 6. SaTor Security Analysis

## 6.1. Adversary Model

SaTor considers two adversaries: relay-level, referring to malicious relays, and network-level, denoting adversarial network service providers. A relay-level adversary may actively manipulate traffic to disrupt Tor functionality [68] or passively analyze metadata, such as packet size and timing, for deanonymization through website fingerprinting techniques [69]. An adversary controlling both the entry and exit relay of a circuit can perform end-to-end correlation attacks to deanonymize users [70]. A network-level adversary typically conducts passive surveillance and may attempt AS-level correlation by observing both ends of circuits from different vantage points [71]. In restrictive scenarios, state-level actors may drop connections to known relays or block Tor protocol signatures, limiting user access to Tor [72]. Multiple network-level adversaries may also collude, increasing their traffic visibility and attack effectiveness.

An adversary’s advantage is measured by the proportion of connections it observes, a prerequisite for most attacks. SaTor’s security implications are assessed using differential advantage, which measures the additional benefit an adversary gains after introducing satellite routing in Tor.

## 6.2. Malicious Relays

SaTor preserves Tor’s default path selection and only opportunistically employs satellite on certain hops within the default circuit. The presence of satellite interfaces does not confer any selection priority. Hence, malicious relays in SaTor appear in circuits with the same probability as in vanilla Tor and gain no additional visibility. While a malicious SaTor relay may attempt to undermine latency benefits by consistently avoiding, or exclusively using, satellite interfaces, such misbehavior is not unique to SaTor. Comparable actions, such as deliberate throttling, can also be carried out by relays in vanilla Tor. Therefore, SaTor is unlikely to increase the capabilities of relay-level adversaries.

## 6.3. Adversarial Satellite Service Provider

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/feec2eeaad3c2e0268b1e87996eddf3efde278ef2be056ec09a0334ba7bbdc9d.jpg)  
(a) Relay-pair Observation

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/2b5c6ed2eda2452a973b93b78a05467764dfa26f14fbb6f734e65b29b88dbd1e.jpg)  
(b) Circuit Observation  
Figure 14: Observable relay pairs and circuits from satellite providers and from major terrestrial providers.

Satellite services are dominated by a few providers, which may act as new network-level adversaries introduced by SaTor. However, in terms of threat model, these satellite providers are fundamentally similar to traditional fiberbased providers. Currently, Tor is unevenly distributed, with many relays hosted by a small number of providers [1]. In SaTor, as long as satellite deployment remains moderate, satellite providers do not gain undue advantage. Fig. 14(a) shows the percentage of relay pairs observable by satellite providers under varying numbers of SaTor relays, alongside the visibility of the two most dominant terrestrial providers.

To match AS1103’s visibility (40% of pairs), the weightedn scenario requires 900 satellite relays, while the top-n scenario requires 350. To reach AS16276’s visibility (70%), both scenarios require over 1k satellite relays.

Circuit observation is defined as the case where the entire entry-to-exit path is visible to the adversary. A terrestrial network operator achieves this simply by hosting a middle relay and observing its ingress and egress traffic. In contrast, a satellite provider must host both the entry and middle, since SaTor uses satellite only for outbound connections. Exits are excluded as Tor disallows one operator from hosting both entry and exit, and SaTor prevents satellite usage at exits. As shown in Fig. 14(b), matching AS24940’s visibility (15.68% of circuits) requires >600 satellite relays in the weighted-n scenario and ≈150 in the top-n.

SaTor could achieve reasonable benefits with ≈100 dualhomed relays, without posing significant advantages to satellite providers. Moreover, SaTor can distribute dual-homed relays across different providers, such as Starlink [42], OneWeb [43], and Amazon Kuiper [73], thereby avoiding excessive visibility by any single entity. Moreover, recall that SaTor only modifies the data forwarding process between entry and exit relays, leaving the connections between client and entry, as well as between exit and destination server, unchanged. Therefore, SaTor does not increase the risk of end-to-end deanonymization attacks, which require a global adversary observing both ends of a circuit. To this end, collusion with satellite providers, whether by other network operators or malicious relays, is similar to collusion with fiber-based providers. Introducing satellite routing into Tor simply implies a small subset of relays migrating to a few new providers—whether satellite or terrestrial-based— without altering Tor’s overall trust model.

## 6.4. Fingerprinting Attacks in SaTor

Attackers can infer the websites users visit by analyzing traffic at entry relays, exploiting the fact that traffic metadata varies across websites. Since satellite transmissions may introduce distinguishable traffic metadata compared to terrestrial links, it is important to reassess SaTor’s vulnerability to website fingerprinting. Encouragingly, a recent study [74] finds that Tor over Starlink is comparably susceptible to website fingerprinting as Tor over fiber. By collecting traffic datasets from both terrestrial and Starlink connections to the Tor network, the study observed that state-of-theart fingerprinting attacks show a ≈2–8% drop in accuracy over satellite links. Furthermore, fingerprinting defenses are similarly, or even more effective on Starlink, reducing attack accuracy by up to 12% more than on fiber.

Satellite traffic may be fingerprinted for relay discovery attacks. For example, an exit relay could infer the use of satellite transmission between the guard and middle by identifying satellite-specific metadata, such as distinctive packet sizes or timing patterns compared to terrestrial routing. If the exit determines that the guard-middle link is on satellite, it may narrow down the guard’s location, since satellite acceleration is often tied to geographical factors, implying that the guard is likely situated far from the middle relay. One possible mitigation is to broaden satellite adoption across more links, allowing relays to use satellite even when it is up to t% slower than terrestrial routing, thereby trading a small performance cost for improved anonymity, which could be a future direction to explore.

## 7. Related Work

Tor’s latency reduction efforts can be categorized as biased or non-biased. The biased approaches prioritize links with lower latency, based on either ad-hoc measuring prior to link selection or historical latency records. Instead of Tor’s default relay-by-relay selection, these approaches often perform circuit-level selection [6], [7], [12], evaluating the overall performance of candidate circuits and assigning higher selection weights to those with lower latency. Such active manipulation on circuit selection often yields notable latency improvements, e.g., PredicTor [7] accelerates 10% of circuits by >1.5 s in PLT, while SaTor achieves only a >600 ms reduction for 10% using 100 weighted-n relays.

However, the biased approaches impose additional predictability to users’ data paths, offering advantages to adversaries. Algorithms favoring geographically short circuits might exacerbate the node-placement attack, wherein adversaries position malicious nodes close to users to increase their chances of being selected [14], [16]. Passive attackers, who deanonymize users by monitoring the latency or speed of a circuit, now only need to observe fewer circuits to make accurate inferences [75], [76]. For Tor, which relies on a large and diverse user base to maintain anonymity, reduction in the randomness of user behavior could heighten deanonymization risk [37], [38], [39].

The non-biased approaches retain Tor’s default path selection algorithm, while modifying the subsequent data routing process. Multi-path routing approaches split traffic across multiple semi-disjoint circuits to avoid single-path congestion, based on the fact that due to the heterogeneity of relay bandwidths, some relays are heavily used while others are less traveled [5], [77]. However, simultaneously using multiple circuits increases vulnerability to end-to-end correlation attacks by broadening the exposure to network-level adversaries and malicious relays, which may deanonymize users by observing just one sub-circuit. In contrast, SaTor does not introduce additional relays or alter the end segments of circuits, thereby avoiding extra correlation risks.

Another non-biased approach, ShorTor, adds extra via relays into standard circuits, to make the newly built circuit faster [8]. Although ShorTor reduces Tor latency without significant security compromises, its effectiveness is largely concentrated in a small fraction of circuits. Concretely, it reduces latency by >100 ms for 1.1% of circuits, >25 ms for 8%, and >10 ms for 11%, while the remaining 90% show no significant reduction. In comparison, SaTor under the weighted-100 scenario improves latency by >100 ms for 0.7% of circuits, >25 ms for 14%, and >10 ms for 24%, with ≈40% of circuits experiencing improvements. Moreover, ShorTor may impose a burden on Tor by requiring some relays to manage traffic that would not ordinarily be routed through them. It consumes ≈100 MB of additional bandwidth per relay per day, while SaTor requires 3 MB.

## 8. Conclusion

High latency remains an essential challenge for Tor. Traditional latency reducing strategies often bias shorter circuits, compromising traffic path randomness and degrading security. This paper explores satellite routing in Tor, outfitting relays with satellite connections, coupled with a dual-homing mechanism to adaptively arrange the usage of satellite and terrestrial interfaces for optimal latency. Our evaluation shows that over a long-term observation, SaTor in general accelerates over 40% circuits by an average of 21.8 ms, with the top 100 most popular relays accessed to satellite network. This study offers a first perspective on utilizing satellite technology to address Tor’s challenges, serving as a reference for Tor’s future improvements.

## Acknowledgement

We thank the anonymous reviewers and shepherd for their insightful feedback. We are grateful to Diogo Barradas at the University of Waterloo for his valuable suggestions and for coordinating the satellite testbed. We further thank Professor Tian Song at the Beijing Institute of Technology, Andrew Ferguson and Mohamad Kassem at the University of Edinburgh for their assistance in improving this work.

## References

[1] The Tor Project, “Tor Metrics.” https://metrics.torproject.org/, 2025. Online.

[2] R. Dingledine, N. Mathewson, P. F. Syverson, et al., “Tor: The second-generation onion router,” in USENIX security symposium, vol. 4, pp. 303–320, 2004.

[3] M. Akhoondi, C. Yu, and H. V. Madhyastha, “LASTor: A low-latency AS-aware Tor client,” in 2012 IEEE Symposium on Security and Privacy, pp. 476–490, IEEE, 2012.

[4] T. Wang, K. Bauer, C. Forero, and I. Goldberg, “Congestion-aware path selection for Tor,” in Financial Cryptography and Data Security: 16th International Conference, FC 2012, Kralendijk, Bonaire, Februray 27-March 2, 2012, Revised Selected Papers 16, pp. 98–113, Springer, 2012.

[5] M. AlSabah, K. Bauer, T. Elahi, and I. Goldberg, “The path less travelled: Overcoming Tor’s bottlenecks with traffic splitting,” in Privacy Enhancing Technologies: 13th International Symposium, PETS 2013, Bloomington, IN, USA, July 10-12, 2013. Proceedings 13, pp. 143– 163, Springer, 2013.

[6] R. Annessi and M. Schmiedecker, “NavigaTor: Finding faster paths to anonymity,” in 2016 IEEE European Symposium on Security and Privacy (EuroS&P), pp. 214–226, IEEE, 2016.

[7] A. Barton, M. Wright, J. Ming, and M. Imani, “Towards predicting efficient and anonymous Tor circuits,” in 27th USENIX Security Symposium (USENIX Security 18), pp. 429–444, 2018.

[8] K. Hogan, S. Servan-Schreiber, Z. Newman, B. Weintraub, C. Nita-Rotaru, and S. Devadas, “ShorTor: Improving Tor network latency via multi-hop overlay routing,” in 2022 IEEE Symposium on Security and Privacy (SP), pp. 1933–1952, IEEE, 2022.

[9] I. Arapakis, X. Bai, and B. B. Cambazoglu, “Impact of response latency on user behavior in Web search,” in Proceedings of the international ACM SIGIR conference on Research & development in information retrieval, pp. 103–112, 2014.

[10] P. Dhungel, M. Steiner, I. Rimac, V. Hilt, and K. W. Ross, “Waiting for anonymity: Understanding delays in the Tor overlay,” in 2010 IEEE Tenth International Conference on Peer-to-Peer Computing (P2P), pp. 1–4, IEEE, 2010.

[11] C. Wacek, H. Tan, K. S. Bauer, and M. Sherr, “An empirical evaluation of relay selection in Tor,” in Proceedings of the Network and Distributed System Security Symposium, 2013.

[12] M. Imani, M. Amirabadi, and M. Wright, “Modified relay selection and circuit selection for faster Tor,” IET Communications, vol. 13, no. 17, pp. 2723–2734, 2019.

[13] P. Mittal, A. Khurshid, J. Juen, M. Caesar, and N. Borisov, “Stealthy traffic analysis of low-latency anonymous communication using throughput fingerprinting,” in Proceedings of the 18th ACM conference on Computer and Communications Security, pp. 215–226, 2011.

[14] G. Wan, A. Johnson, R. Wails, S. Wagh, and P. Mittal, “Guard placement attacks on path selection algorithms for Tor,” Proceedings on Privacy Enhancing Technologies, vol. 2019, no. 4, 2019.

[15] I. Karunanayake, N. Ahmed, R. Malaney, R. Islam, and S. K. Jha, “De-anonymisation attacks on Tor: A survey,” IEEE Communications Surveys & Tutorials, vol. 23, no. 4, pp. 2324–2350, 2021.

[16] Q. Tan, X. Wang, W. Shi, J. Tang, and Z. Tian, “An anonymity vulnerability in Tor,” IEEE/ACM Transactions on Networking, vol. 30, no. 6, pp. 2574–2587, 2022.

[17] C. Incorporated, “Smf-28tm optical fiber product information,” 2002.

[18] A. U. Chaudhry and H. Yanikomeroglu, “Optical wireless satellite networks versus optical fiber terrestrial networks: The latency perspective: Invited chapter,” in 30th Biennial Symposium on Communications 2021, pp. 225–234, Springer, 2022.

[19] M. Handley, “Delay is not an option: Low latency routing in space,” in Proceedings of the 17th ACM Workshop on Hot Topics in Networks, pp. 85–91, 2018.

[20] M. Handley, “Using ground relays for low-latency wide-area routing in megaconstellations,” in Proceedings of the 18th ACM Workshop on Hot Topics in Networks, pp. 125–132, 2019.

[21] I. N. Bozkurt, A. Aguirre, B. Chandrasekaran, P. B. Godfrey, G. Laughlin, B. Maggs, and A. Singla, “Why is the Internet so slow?!,” in Passive and Active Measurement: 18th International Conference, PAM 2017, Sydney, NSW, Australia, March 30-31, 2017, Proceedings 18, pp. 173–187, Springer, 2017.

[22] T. Høiland-Jørgensen, B. Ahlgren, P. Hurtig, and A. Brunstrom, “Measuring latency variation in the Internet,” in Proceedings of the 12th International on Conference on emerging Networking EXperiments and Technologies, pp. 473–480, 2016.

[23] J. Chavula, A. Phokeer, A. Formoso, and N. Feamster, “Insight into Africa’s country-level latencies,” in IEEE AFRICON 2017, pp. 938– 944, Institute of Electrical and Electronics Engineers Inc., 2017.

[24] J. Zhao and J. Pan, “LENS: A LEO satellite network measurement dataset,” in Proceedings of the 15th ACM Multimedia Systems Conference, pp. 278–284, 2024.

[25] RIPE, “RIPE Atlas.” https://atlas.ripe.net/, 2024.

[26] Z. Lai, H. Li, and J. Li, “StarPerf: Characterizing network performance for emerging mega-constellations,” in 2020 IEEE 28th International Conference on Network Protocols (ICNP), pp. 1–11, IEEE, 2020.

[27] Z. Lai, H. Li, Y. Deng, Q. Wu, J. Liu, Y. Li, J. Li, L. Liu, W. Liu, and J. Wu, “StarryNet: Empowering researchers to evaluate futuristic integrated space and terrestrial networks,” in 20th USENIX Symposium on Networked Systems Design and Implementation (NSDI 23), pp. 1309–1324, 2023.

[28] S. Kassing, D. Bhattacherjee, A. B. Aguas, J. E. Saethre, and<sup>´</sup> A. Singla, “Exploring the Internet from space with Hypatia,” in Proceedings of the ACM Internet Measurement conference, pp. 214– 229, 2020.

[29] A. Cloud, “Performance monitoring metrics.” https://www.alibabaclo ud.com/help/en/well-architected/latest/performance-monitoring-indi cators/, 2025. Online.

[30] Starlink, “Starlink service plans.” https://www.starlink.com/service-p lans/, 2025. Online.

[31] D. Mohney, “The space cloud: Satellite strategies for AWS, Google and Microsoft.” https://www.datacenterfrontier.com/cloud/article/114 28161/the-space-cloud-satellite-strategies-for-aws-google-and-micr osoft, 2021.

[32] A. Raj, “How satellites are becoming a game changer for cloud service providers.” https://techwireasia.com/03/2023/heres-how-s atellites-are-enhancing-connectivity-for-cloud-service-providers/, 2023.

[33] M. G. Reed, P. F. Syverson, and D. M. Goldschlag, “Anonymous connections and onion routing,” IEEE Journal on Selected areas in Communications, vol. 16, no. 4, pp. 482–494, 1998.

[34] M. AlSabah and I. Goldberg, “Performance and security improvements for Tor: A survey,” ACM Computing Surveys (CSUR), vol. 49, no. 2, pp. 1–36, 2016.

[35] R. Jansen, P. Syverson, and N. Hopper, “Throttling Tor bandwidth parasites,” in 21st USENIX Security Symposium (USENIX Security 12), pp. 349–363, 2012.

[36] R. Dingledine and N. Mathewson, “Tor specifications,” 2023

[37] M. Backes, A. Kate, S. Meiser, and E. Mohammadi, “(Nothing else) MATor(s): Monitoring the Anonymity of Tor’s Path Selection,” in Proceedings of the 21th ACM conference on Computer and Communications Security (CCS 2014), November 2014.

[38] M. Backes, S. Meiser, and M. Slowik, “Your Choice MATor(s): Largescale quantitative anonymity assessment of Tor path selection algorithms against structural attacks,” Proceedings on Privacy Enhancing Technologies, vol. 2016, April 2016.

[39] J. Juen, A. Johnson, A. Das, N. Borisov, and M. Caesar, “Defending Tor from network adversaries: A case study of network path prediction,” Proceedings on Privacy Enhancing Technologies, vol. 2015, no. 2, pp. 1–17, 2015.

[40] SpaceX FCC update, “SPACEX NON-GEOSTATIONARY SATEL-LITE SYSTEM.” https://licensing.fcc.gov/myibfs/download.do?attac hment key=1569860, 2018. Online.

[41] J. McDowell, “Jonathan’s Space Report.” https://planet4589.org/, 2025. Online.

[42] SpaceX, “Starlink.” https://www.starlink.com/, 2025. Online.

[43] OneWeb, “Oneweb.” https://oneweb.net/, 2025. Online.

[44] A. U. Chaudhry and H. Yanikomeroglu, “On crossover distance for optical wireless satellite networks and optical fiber terrestrial networks,” in 2022 IEEE Future Networks World Forum (FNWF), pp. 480–485, IEEE, 2022.

[45] M. M. Kassem, A. Raman, D. Perino, and N. Sastry, “A browserside view of Starlink connectivity,” in Proceedings of the 22nd ACM Internet Measurement Conference, pp. 151–158, 2022.

[46] S. Ma, Y. C. Chou, H. Zhao, L. Chen, X. Ma, and J. Liu, “Network characteristics of LEO satellite constellations: A Starlink-based measurement from end users,” in IEEE INFOCOM 2023-IEEE Conference on Computer Communications, pp. 1–10, IEEE, 2023.

[47] N. Mohan, A. Ferguson, H. Cech, P. R. Renatin, R. Bose, M. Marina, and J. Ott, “A multifaceted look at Starlink performance,” in Proceedings of the ACM Web Conference 2024 (WWW ’24), 2024.

[48] T. Kelso, “CelesTrak: Current NORAD two-line element sets.” https: //www.celestrak.com/NORAD/elements/, 2024.

[49] S. Insider, “Starlink ground station locations: An overview.” https: //starlinkinsider.com/starlink-gateway-locations, 2024. Online.

[50] Space-Track Team, “Space-track.” https://www.space- track.org/, 2024. Online.

[51] MaxMind, “GeoIP accuracy comparison.” https://www.maxmind.co m/en/geoip-accuracy-comparison, 2024.

[52] M. Maltsev, “Stem.” https://github.com/torproject/stem, 2023.

[53] A. Johnson, C. Wacek, R. Jansen, M. Sherr, and P. Syverson, “Users get routed: Traffic correlation on Tor by realistic adversaries,” in Proceedings of the 20th ACM Conference on Computer and Communications Security, 2013.

[54] J. Y. Yen, “Finding the k shortest loopless paths in a network,” management Science, vol. 17, no. 11, pp. 712–716, 1971.

[55] K. Linux, “hping3.” https://www.kali.org/tools/hping3/, 2024.

[56] Medium, “Statistics behind latency metrics: Understanding p90, p95, and p99.” https://medium.com/tuanhdotnet/statistics-behind-laten cy-metrics-understanding-p90-p95-and-p99-dc87420d505d/, 2024. Online.

[57] F. Cangialosi, D. Levin, and N. Spring, “Ting: Measuring and exploiting latencies between all tor nodes,” in Proceedings of the 2015 Internet Measurement Conference, pp. 289–302, 2015.

[58] L. Izhikevich, M. Tran, K. Izhikevich, G. Akiwate, and Z. Durumeric, “Democratizing LEO satellite network measurement,” Proceedings of the ACM on Measurement and Analysis ofComputing Systems, vol. 8, no. 1, pp. 1–26, 2024.

[59] T. Pan, G. Ruan, Q. Fu, Z. Luo, J. Huang, X. Luo, and T. Huang, “Stableroute: When dijkstra’s algorithm meets topology-varying satellite networks,” in IEEE INFOCOM 2025-IEEE Conference on Computer Communications, pp. 1–10, IEEE, 2025.

[60] CableTV, “Best fiber internet providers: Prices, speeds, and more.” https://www.cabletv.com/internet/best-fiber-internet-providers/, 2025. Online.

[61] The Tor Project, “Relay requirements.” https://community.torproject .org/relay/relays-requirements/, 2024. Online.

[62] IPinfo, “IPinfo: Trusted IP data provider.” https://ipinfo.io/, 2024.

[63] R. Gupta, “Can starlink support multiple users simultaneously?.” ht tps://spacetek.com.au/blogs/news/can-starlink-support-multiple-users -simultaneously, 2024. Online.

[64] Alsmith, “Transparency, openness, and our 2021-2022 financials.” ht tps://blog.torproject.org/transparency-openness-and-our-2021-and-2 022-financials/, 2023. Online.

[65] S. Leibfarth, “torservers.net.” https://torservers.net/, 2025. Online.

[66] R. Fanou, F. Valera, and A. Dhamdhere, “Investigating the causes of congestion on the African IXP substrate,” in Proceedings of the 2017 Internet Measurement Conference, pp. 57–63, 2017.

[67] R. Fontugne, A. Shah, and K. Cho, “Persistent last-mile congestion: Not so uncommon,” in Proceedings ofthe ACM internet measurement conference, pp. 420–427, 2020.

[68] C. Sendner, J. Stang, A. Dmitrienko, R. Wijewickrama, and M. Jadliwala, “MirageFlow: A new bandwidth inflation attack on Tor,” in Network and Distributed System Security (NDSS) Symposium, 2024.

[69] N. Mathews, J. K. Holland, S. E. Oh, M. S. Rahman, N. Hopper, and M. Wright, “Sok: A critical evaluation of efficient website fingerprinting defenses,” in 2023 IEEE Symposium on Security and Privacy (SP), pp. 969–986, IEEE, 2023.

[70] S. E. Oh, T. Yang, N. Mathews, J. K. Holland, M. S. Rahman, N. Hopper, and M. Wright, “DeepCoFFEA: Improved flow correlation attacks on Tor via metric learning and amplification,” in 2022 IEEE Symposium on Security and Privacy (SP), pp. 1915–1932, IEEE, 2022.

[71] Y. Sun, A. Edmundson, N. Feamster, M. Chiang, and P. Mittal, “Counter-RAPTOR: Safeguarding Tor against active routing attacks,” in 2017 IEEE Symposium on Security and Privacy (SP), pp. 977–992, IEEE, 2017.

[72] A. Master and C. Garman, “A worldwide view of nation-state Internet censorship,” Free and Open Communications on the Internet, 2023.

[73] Amazon, “Project Kuiper.” https://www.aboutamazon.com/what-wedo/devices-services/project-kuiper/, 2025. Online.

[74] P. Singh, D. Barradas, T. Elahi, and N. Limam, “Connecting the dots in the sky: Website fingerprinting in low earth orbit satellite Internet,” Network and Distributed System Security Symposium (NDSS), 2024.

[75] M. Nasr, A. Bahramali, and A. Houmansadr, “DeepCorr: Strong flow correlation attacks on Tor using deep learning,” in Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, pp. 1962–1976, 2018.

[76] F. Rochet and O. Pereira, “Dropping on the edge: Flexibility and traffic confirmation in onion routing protocols.,” Proceedings on Privacy Enhancing Technology, vol. 2018, no. 2, pp. 27–46, 2018.

[77] L. Yang and F. Li, “mTor: A multipath Tor routing beyond bandwidth throttling,” in 2015 IEEE Conference on Communications and Network Security (CNS), pp. 479–487, IEEE, 2015.

## Appendix A.

## Baseline Latency Measurement

Baseline Latency Dataset. Table 4 shows the satellite latency data collected from LENS dataset. The measurements were conducted across five geographical locations: Alaska, Frankfurt, Seattle, Vancouver, and Victoria. Seattle has two dishes subscribing to Starlink’s regular and highpriority service plan. We extract a total 1.624 billion data points of ICMP latencies from the LENS dataset, spanning a two-month period from April to May, 2024. As of terrestrial latency, as listed in Table 5, we extract over 104.64 million data points from RIPE dataset, covering a one-week period starting on Sep. 2, 2024. The data is divided based on the round-trip length, by a 2k kilometers interval.

TABLE 4: Baseline Satellite Latency from LENS Dataset

<table><tr><td>Dish Loc.</td><td>PoP Loc.</td><td>Route Len. (km)</td><td>Duration</td><td>Data Num.</td></tr><tr><td>Alaska</td><td>Seattle</td><td>5,119</td><td>26 days</td><td>134.81M</td></tr><tr><td>Frankfurt</td><td>Frankfurt</td><td>2,200</td><td>40 days</td><td>227.58M</td></tr><tr><td>Seattle</td><td>Seattle</td><td>2,200</td><td>46 days</td><td>264.89M</td></tr><tr><td>Seattle_hp</td><td>Seattle</td><td>2,200</td><td>54 days</td><td>327.21M</td></tr><tr><td>Vancouver</td><td>Seattle</td><td>2,234</td><td>59 days</td><td>333.94M</td></tr><tr><td>Victoria</td><td>Seattle</td><td>2,212</td><td>61 days</td><td>339.97M</td></tr></table>

TABLE 5: Baseline Terrestrial Latency from RIPE Dataset

<table><tr><td>Traffic Route Length (km)</td><td>Pairs Number</td><td>Data Number</td></tr><tr><td>0–2k</td><td>213,752</td><td>56.98M</td></tr><tr><td>2k–4k</td><td>55,388</td><td>13.23M</td></tr><tr><td>4k–6k</td><td>49,656</td><td>12.15M</td></tr><tr><td>6k–8k</td><td>96,827</td><td>22.28M</td></tr><tr><td>Total</td><td>415,623</td><td>104.64M</td></tr></table>

Baseline Traffic Speed. The CDFs for the speed of satellite and terrestrial traffic are derived from LENS and RIPE datasets. The latencies are measured using ICMP transmissions, capturing all practical latency components. They also reflect the influence of factors such as satellite movement, weather conditions, and network reconfiguration [47]. Continuously sampling from this CDF over an extended duration can replicate the long-term latency characteristics of satellite and terrestrial routing at a global scale.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/1857428d1fcff70b03ababbc5d0c0976b2f2f522e26de1b77c7f74d89d03e940.jpg)  
(a) LENS (Starlink)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/a7815de3ce04cc1fb216c3db32de2a21cea3d60410ad70a3db4a47b7de10a494.jpg)  
(b) RIPE (Terrestrial)  
Figure 15: Traffic speed CDF of LENS and RIPE Dataset.

Fig. 15(a) presents the satellite traffic speed across five locations. Seattle includes two dishes with regular and highpriority subscriptions, with the latter expected to show better latency performance. The round-trip length of satellite traffic is ≈ 2,200 km, except for Alaska, which is ≈5,119 km. Vancouver (light purple curve) exhibits the slowest traffic speed, while Frankfurt (light red) and Seattle’s priority dish (light green) demonstrate the best speed performance. Traffic speed differences across global locations may result from the varying density of the satellite constellation, ground stations, and dish performance. The combinatorial CDF across all locations (black curve) shows that satellite traffic transmits slower than 50k km/s during ≈ 15% of the time, and slower than 100k km/s during ≈ 85% of the time.

Terrestrial traffic speeds are measured across ≈12,000 global probes on the RIPE Atlas platform. The distances between probe pairs range from 0.06 to 10k km (roundtrip route lengths of 0.12 to 20k km). These figures are straight-line end-to-end distances, disregarding the routing detours through intermediate devices. Fig. 15(b) indicates that shorter round-trip corresponds to slower traffic. When round-trip lengths are between 0-4k km (the transparent black curve) the speed CDF is above all other curves, meaning that a larger portion of the data is concentrated within the lower speed range. In contrast, transmissions >8k km (transparent blue curve) exhibit the fastest traffic speeds among all groups, probably because very long-distance transmissions, such as links between Europe and America, often utilize high-capacity backbone connections optimized for global communication, whereas shorter transmissions may experience suboptimal inter-domain routing.

## Appendix B. Satellite Routing Strategy

A routing graph model is used for simulating satellite routing latency between two nodes, detailed below.

Routing Graph Nodes. User means the sending and receiving party of satellite communication. In Tor, this could be a client, relay and destination server. Satellite circles the Earth at a fixed altitude, acting as a “mirror” to reflect or forward signals without processing or caching. Ground Station, equipped with antennas and electronic transmitters, directly communicates with satellites for tracking, controlling and data relaying. Point of Presence (PoP) acts as a gateway between satellite and terrestrial networks. Traffic from satellites must pass through a ground station, and then a PoP before entering the terrestrial Internet.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/019a1dc05bbeb42cd9a82ae0d786146345d4ce587beeb9e4a96db14a8cb88a80.jpg)  
(a) Possible Link Types

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/637a95925465fdd1d9313a53267fac00d5df8d9e493a5aafc5fd0cd56e5b37fd.jpg)

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/bbff08b64758518cd66487aaa60ec1105cfefac86d7df263a75aa136485854f9.jpg)  
(c) Single Bent-pipe Routing

(b) Traditional Terrestrial Routing  
![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/ae6f2eafb2e2cd7ce1c8eb1c3e9adbed7e1435cdb8e1bdc6a0f48eddb7c11126.jpg)  
(d) ISL-enabled Routing  
Figure 16: Routing graph between relays. Black line indicates available links while gray means unavailable ones.

Routing Graph Edges. As shown in Fig. 16(a), Inter-User Link (IUL, link 1) connects users through the terrestrial Internet. User-Satellite Link (USL, link 2) carries data from a user to a nearby satellite via spot-beams through the atmosphere. Inter-Satellite Link (ISL, link 3) is a laser-based connection between satellites, transmitting at the speed of light in vacuum. Groundstation-Satellite Link (GSL, link 4) exchanges traffic between satellites and ground stations using spot-beams. Groundstation-PoP Link (GPL, link 5) connects ground stations to nearby PoPs before traffic enters the terrestrial Internet, with a global latency of about 5 ms [47]. Finally, User-PoP Link (UPL, link 6) delivers traffic between PoPs and users over the terrestrial Internet.

Routing Strategies. Fig. 16(b) illustrates terrestrial routing, where neither relay connects to the satellite network and only IUL is used. In Fig. 16(c), USL, GSL, GPL, and UPL are available, forming a “bent-pipe” structure: traffic from the source relay travels to satellite-1, down to a nearby ground station, then proceeds to the PoP and destination via the terrestrial network. When ISLs are available, as shown in Fig. 16(d), traffic is relayed across multiple satellites before descending to a ground station near the destination. This “ISL-enabled” routing keeps data in space for most of its journey, fully exploiting satellite acceleration potential.

## Appendix C.

## Satellite Routing across Varying Distance

Fig. 17 shows SaTor’s latency reduction grouped by end-to-end geographic distance. Satellite routing achieves the greatest gains in the 5–6k km (57%) ranges. Moderate improvements (20–40%) are observed at 8–10k km and 0.5- 1k km. An intuitive explanation is that, for connections shorter than 0.5k km, terrestrial routing is already fast, while bent-pipe satellite links add propagation overhead. In the 0.5–1k km range, terrestrial delays are inflated due to local congestion or inefficient routing across regional ASes. Between 1k and 3k km, terrestrial traffic might be handed off to Tier-1 backbones, enabling optimized routing to reduce AS-path inflation. The 5–6k km range often involves transoceanic links, where terrestrial routes may experience congestion during suboptimal cable routing, while intersatellite links can provide more stable and direct delivery. Beyond 6k km, the satellite advantage diminishes, possibly due to increased ISL hops and routing inefficiencies.

![](../01-mineru-output/2026-S%26P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/images/51f7f85638af8465dcaf29102db10d6f9558bdc4aaf953a4a4615d46ad5f34bb.jpg)  
Endpoint Straight-line Distance (km)  
Figure 17: SaTor latency reduction efficacy across varying end-to-end distance between relay pairs.

## Appendix D.

## SaTor in the Real World

According to SpaceX’s website, Starlink services are currently offered in over 65 countries. As of December 2024, out of 8,730 Tor relays in total, 8,280 (94%) are situated in countries where Starlink is operational, demonstrating the practicality of SaTor under current conditions.

Based on Tor Metrics [1] and IPinfo database [62], all relay ASes are categorized into four types: cloud platform, general ISP, business network, and education network. As Table 6 shows, cloud platforms host 60% of the top 2k relays and 70% of all relays. Deploying SaTor on cloudhosted relays would require the cloud providers to access their platform to satellite networks. Fortunately, major cloud providers are moving in that direction. Cloud providers like Amazon, Google, and Microsoft are cooperating with satellite companies to enhance their service [31], [32]. About 30% of relays are hosted on general ISP, business, or education networks, where SaTor deployment could be more straightforward. Around 40% of the top 2k relays are noncloud, which is sufficient to realize SaTor’s potential.

TABLE 6: AS Type of Tor Relays

<table><tr><td>AS Type</td><td>Top-2k</td><td>Top-4k</td><td>Top-6k</td><td>All (8,730)</td></tr><tr><td>Cloud Platform</td><td>1,199 (60%)</td><td>2,886 (72%)</td><td>4,393 (73%)</td><td>6,149 (70%)</td></tr><tr><td>General ISP</td><td>422 (21%)</td><td>571 (14%)</td><td>887 (15%)</td><td>1,771 (20%)</td></tr><tr><td>Business</td><td>66 (3%)</td><td>97 (2%)</td><td>233 (4%)</td><td>249 (3%)</td></tr><tr><td>Education</td><td>313 (16%)</td><td>445 (12%)</td><td>485 (8%)</td><td>559 (7%)</td></tr></table>

## Appendix E. Meta-Review

The following meta-review was prepared by the program committee for the 2026 IEEE Symposium on Security and Privacy (S&P) as part of the review process as detailed in the call for papers.

## E.1. Summary

This paper presents SaTor, a system for reducing latency in Tor by routing through satellite systems such as Starlink. In SaTor, participating relays are dual-homed—they can send traffic either along terrestrial links or through satellite links.

The authors collected real-world routing and satellite data and used these to build a simulator to estimate the benefits of such an approach. Their simulations suggest that significant speedups could be had for large portions of the Tor network, even if only a small percentage of relays adopt this approach.

## E.2. Scientific Contributions

Provides a Valuable Step Forward in an Established Field

## E.3. Reasons for Acceptance

1) Provides a Valuable Step Forward in an Established Field. Latency in Tor has been a research topic for a long time, but it is still far from solved. Prior works have used other schemes to route data on alternate paths, but this work was able to do so without leaking any additional information to a global adversary.

## E.4. Noteworthy Concerns

1) The paper’s model for performance is based on data from a single satellite link, and it appears that the evaluated configuration doesn’t 100% mirror the proposed one.

2) The authors present an optimistic pathway for adoption, which while possible, might still prove too burdensome for widespread use.