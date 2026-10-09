# Breaking the Accuracy-Latency Trade-Off in Sketch Compression for Network Measurement

Hui Yu $^{1}$ , Tao Zhang $^{1,2*}$ , Siyuan Fan $^{1}$ , Ziyi Liu $^{1}$ , Zhihong Wang $^{1}$ , Yunsheng Liu $^{1}$ , Linfei Dong $^{1}$ , Haozhi Tang $^{1}$ , Ao Zhang $^{1}$ , Hui Yin $^{1,2}$ , and Fangmin Li $^{1,2}$

$^{1}$ School of Computer Science and Engineering, Changsha University, Changsha, China $^{2}$ Hunan Province Key Laboratory of Industrial Internet Technology and Security, Changsha, China  
Corresponding author: Tao Zhang. Email: tzhang@ccsu.edu.cn.

Abstract—Sketch-based measurement is fundamental for real-time network monitoring, but performing efficient, high-fidelity compression for distributed sketch aggregation remains a critical bottleneck. Current methods present a severe trade-off: grouping-based techniques (e.g., Elastic, Hokusai) are fast but incur unbounded errors, while clustering-based approaches improve accuracy at the cost of prohibitive latency, making neither suitable for real-time control loops. This paper introduces LightRanger (LR), a lightweight compression mechanism designed to break the above trade-off. LightRanger is built on two key designs: (1) real-time value-range grouping, which dynamically sets grouping intervals using observed global extrema to enable low-distortion, uniform bucket mapping; and (2) adaptive bitmap pruning, which strategically reduces transmission overhead under strict bandwidth limits while preserving essential statistical structure. Evaluated across real-world traces (i.e., CAIDA, MAWI, Zipf, and Webdocs) and standard sketches including Count-Min (CM) Sketch, Count-Mean-Min (CMM) Sketch, Conversation-Update (CU) Sketch, and CSM Sketch, LightRanger reduces average relative error by up to 8.92× over Elastic and 38.59× over Hokusai, while running 37.23× faster than clustering-based methods. By decoupling accuracy from latency, LR makes high-fidelity, real-time sketch aggregation practical for bandwidth-constrained distributed monitoring.

Index Terms—Sketch compression, adaptive quantization, bandwidth-efficient aggregation.

## I. INTRODUCTION

Network measurement lies at the core of operating and evolving modern infrastructures, underpinning critical tasks from traffic engineering and security monitoring to service assurance $[1]$ . To keep pace with line-rate traffic, sketches have emerged as an indispensable algorithmic primitive. They leverage theoretical guarantees of sub-linear memory and constant-time updates to maintain provably approximate summaries of high-volume streams, enabling fundamental operations like frequency estimation and heavy hitter detection $[2]$ . Their deployment is now widespread in distributed systems for real-time coordination and optimization.

In distributed monitoring architectures, sketches generated at edge nodes must be periodically aggregated at a central controller to derive a global network view (see Fig. 1). Here, bandwidth forms an inescapable bottleneck [3]. Transmitting raw sketches consumes significant capacity, thereby increasing aggregation latency, exacerbating congestion, and most critically, impairing the timeliness of analytics. During fault or attack scenarios, such delays can directly compromise response efficacy. Consequently, efficient sketch compression is not merely an optimization but a necessary step to ensure the scalability and responsiveness of distributed measurement systems [4]–[8].

![](images/3b2dd235032491e29155c6e081d5e841f7ae0ab3fd980dca46fca6a34c3c8ccb.jpg)  
Fig. 1: Distributed sketch aggregation.

An effective sketch compression scheme must simultaneously address two core constraints: estimation accuracy, to minimize error introduced by the compression process; and compression latency, to support real-time aggregation in distributed pipelines. Existing methodologies, however, present a disjoint trade-off, failing to deliver on all fronts concurrently. Accuracy is significantly degraded by speed-optimized techniques. Group-based compression schemes like Elastic [6] and Hokusai [7] employ simple aggregation heuristics (e.g., summation or max selection within fixed groups), which introduce substantial and unbounded estimation error, rendering the compressed data unreliable for fine-grained analysis. However, latency becomes prohibitive when pursuing accuracy. While clustering improves fidelity over naive grouping, it incurs severe computational cost. Optimal partition strategies based on dynamic programming exhibit quadratic time complexity, and iterative clustering algorithms require multiple convergence passes [8]. Consequently, compression times can escalate from seconds to minutes, far exceeding the sub-second or millisecond latencies mandated for real-time monitoring and control. Thus, the current landscape offers no integrated solution that achieves the necessary balance, creating a critical gap between theoretical compression goals and practical deployability.

In this paper, we present LightRanger, a lightweight sketch compression mechanism designed to break the accuracy-latency dilemma in distributed network measurement. Unlike existing approaches, LightRanger introduces two key designs: (1) a real-time, adaptive value-range grouping strategy that dynamically determines uniform bucket mapping intervals based on observed bucket extremas, enabling fast and low-distortion compression; and (2) an adaptive bitmap pruning technique that selectively retains significant bits under strict bandwidth constraints, ensuring high reconstruction fidelity. By jointly optimizing for transmission overhead and computational efficiency, LightRanger enables high-fidelity, real-time sketch aggregation critical for responsive network control.

Our core contributions are as follows:

\- We characterize the fundamental trade-off in prior work: group-based methods (e.g., Elastic, Hokusai) trade accuracy for speed, while clustering-based approaches (e.g., Cluster-Reduce) achieve better fidelity at the cost of prohibitive latency, neither meets practical requirements.

\- We propose a sketch compression mechanism that integrates two novel techniques: (1) real-time value-range grouping, which dynamically determines grouping intervals based on observed bucket extrema within a measurement epoch, enabling fast, low-distortion bucket mapping; and (2) adaptive bitmap pruning, which prioritizes significant bits under tight bandwidth constraints and uses a lightweight row-distribution indicator to recover pruned low-order data, preserving high query accuracy even at aggressive compression ratios.

\- Using four public traffic traces (CAIDA, MAWI, Zipf, and Webdocs) and four standard sketches (CM, CMM, CU, and CSM), our experiments show that LightRanger reduces average relative error by up to 8.92× over Elastic and 38.59× over Hokusai, while compressing approximately 37.23× faster than clustering-based methods, demonstrating its practical effectiveness.

The rest of this paper is structured as follows. Section II presents the motivation and background. Section III details the design and implementation of our compression framework. Section IV presents theoretical analysis. Section V evaluates LightRanger through extensive experiments. Section VI reviews related work. Section VII concludes this paper.

## II. BACKGROUND AND MOTIVATION

Periodic aggregation of distributed sketches generates substantial reporting traffic, competing for scarce bandwidth, especially during congestion or failure episodes when timely data is most critical $[9]$ , $[10]$ . Efficient compression that preserves measurement fidelity is thus essential for scalable monitoring $[11]$ – $[13]$ . However, existing methods expose a fundamental tension: they sacrifice accuracy for speed, or incur prohibitive computational overhead to maintain precision, thus failing to satisfy both requirements simultaneously. This unresolved trade-off leaves a core bottleneck in practical.

![](images/c65d65083418f3fbc583c35757ef4ed02cc684fc27aa05ffe724f2eb9b6fa7f7.jpg)  
(a) Hokusai

![](images/3ec584d73ac8b3462e16b09c207820dbfe239ad645f2bdc2922e4d6b6e3c997c.jpg)  
(b) Elastic  
Fig. 2: Grouping-based sketch compression schemes.

## A. Measurement Distortion from Lossy Compression

Existing compression-oriented schemes such as Hokusai and Elastic prioritize processing speed by employing simple operations, e.g., consecutive bucket grouping, summation, or max-value merging, yet sacrifice measurement accuracy $[6]$ , $[7]$ . A key issue stems from the inherent randomness of hash functions, which leads to a highly skewed distribution of traffic across sketch buckets. As a matter of fact, in real traffic, bucket values often follow a heavy-tailed distribution (e.g., Zipf), where many buckets contain small values while a few hold very large ones $[14]$ . Consequently, consecutive buckets in a sketch may differ by orders of magnitude, and indiscriminate coarse-grained aggregation erases fine-grained flow distinctions, introducing substantial and uncontrolled error.

To illustrate, consider a typical bucket array extracted from real traffic trace with a target compression ratio of 4 (see Fig. 2). Hokusai, for instance, aggregates consecutive buckets through summation (e.g., summing 9, 35, 4, and 8 into 56 in G2). This approach ignores the underlying flow distribution, as high- and low-frequency items are merged indiscriminately. The resulting value loses all statistical resemblance to the original fine-grained data, introducing severe distortion that propagates and amplifies during later aggregation stages, ultimately corrupting the final measurement. Elastic, in contrast, selects the maximum value within a group to represent it (e.g., representing G1 with the value 80). While reducing aggregation overhead, this method generates unacceptable error when group variance is high, which is common due to hash skew.

Such measurement distortion introduces severe operational risks. In DDoS mitigation, it may trigger false positives by misclassifying normal flows as attack traffic. In traffic engineering, it undermines flow-aware scheduling by obscuring the distinction between elephant and mouse flows. At a systemic level, distorted data can mislead operational decisions, propagate failures, and ultimately compromise the integrity of the entire monitoring-and-control loop.

## B. High Time-Memory Cost of Precision Enhancement

Clustering-based compression techniques, while attempting to improve estimation fidelity, inherently compromise the core computational advantages of sketches: their sub-linear memory footprint and support for line-speed updates and queries.

![](images/4a34d06986613f1c3de10616ab9daaaadca70f05afb4d5d86c7eac5e661a2061.jpg)  
Fig. 3: Typical clustering-based sketch compression scheme.

Cluster-Reduce [8] proposes a precision-recovery mechanism via a multi-stage process, as shown in Fig. 3. First, the original sketch is partitioned into fixed adjacent groups (G1-G4). Then, a clustering algorithm dynamically reorganizes buckets with similar values across these groups into new clusters (C1-C5). The maximum value within each cluster is then selected as its representative (e.g., C1→32, C2→12), while an auxiliary indicator array records the cluster assignment for every original bucket (e.g., “0011” for G1, where bit 0 indicates the left category and bit 1 indicates the right category). Finally, compression is achieved by storing only the representative values and the compact indicator array.

While improving accuracy over grouping-based schemes, clustering-based methods incur prohibitive computational overhead. Cluster-Reduce relies on an exact optimal partition strategy, typically implemented via dynamic programming. In practice, compression latency grows quadratically: processing 10k buckets takes milliseconds, 100k buckets extends to tens of seconds, and at the million-bucket scale (common in core network nodes), delay reaches minutes. This violates the sub-second response requirement of high-speed monitoring, making clustering-based schemes impractical.

## C. Experimental Verification

We evaluate the performance of existing sketch compression methods using real network traffic to quantify their limitations. Our experiments are designed to measure both accuracy and speed across different compression ratios.

Datasets and Sketch Structure. We use packet traces from the CAIDA 2019 dataset [15] and implement CM Sketch [16], a standard structure for frequency estimation.

Compared Methods. We include three representative baselines: Hokusai, Elastic, and two variants of the clustering-based Cluster-Reduce, one using optimal dynamic programming (DP) and another employing iterative clustering (IC-3).

Metrics. We report Average Relative Error (ARE): it is calculated as $1/W \sum_{i=1}^{W} |\hat{b}_{i} - b_{i}|/b_{i}$ , which measures the compression accuracy, and Compression Time (CT): it measures the real-time performance of the compression process.

![](images/6ae0e41bcea70bf55b32013dcdde94615eca4cb9e0712ffbd88edf6d437e48e9.jpg)

![](images/b5cab4b11bc5bd60a0d862835ce1090fdb96d799f5c86daab94687ccb89ad053.jpg)  
(a) Low compression ratio.

![](images/8f42649699c771d8debe1a43f54c11eacfa5aeb2f9aa14b45190fc5182e99522.jpg)

![](images/9d7d4ac93e72881d4ce1d5749ab92fe1242678e2994081bc5a330c351206e464.jpg)  
(b) Medium compression ratio.

![](images/b2874b3207db96f8644430560eb656566d55cbbd2ce2c554b1988d3725419fb9.jpg)

![](images/144ff02006bffdfb9136477c1769c24dd089b5d7f24f91bd17ad003315a95e69.jpg)  
(c) High compression ratio.  
Fig. 4: Comparison of compression accuracy and speed.

Compression Ratios. Tests are conducted at compression ratios of 3 (low), 6 (medium), and 9 (high) to simulate different bandwidth budgets.

Platform. All code is written in C++ and runs on a server with an AMD Ryzen 9 3950X 3.5GHz (up to 4.7GHz) processor and 128GB DDR4 memory.

Results. In Fig. 4, Hokusai and Elastic exhibit significantly higher ARE than DP and IC-3. At the low compression ratio, the ARE for Hokusai and Elastic remains consistently high regardless of sketch size (2-10MB), indicating a fundamental accuracy limitation. In contrast, DP and IC-3 maintain substantially lower error rates by leveraging value-aware clustering. At the medium compression ratio, the error of Hokusai and Elastic surges further, while clustering methods experience only a moderate increase, preserving a clear accuracy advantage. At the high compression ratio, the accuracy imbalance becomes severe. Grouping methods fail to provide reliable estimates, whereas clustering methods, despite increased error, remain significantly more accurate. Compression time reveals the opposite trend. Hokusai and Elastic maintain stable, ultra-low latencies across all sketch sizes and compression ratios, demonstrating their computational efficiency. In contrast, the time cost for DP and IC-3 grows substantially with both sketch size and compression ratio, rendering these approaches unsuitable for real-time aggregation.

Summary. These results confirm an irreconcilable trade-off: grouping-based schemes achieve line-rate compression but incur unbounded errors, while clustering-based methods improve accuracy at the cost of prohibitive and variable latency. This gap underscores the critical need for a new compression mechanism that can simultaneously deliver high accuracy, predictable low latency, and bandwidth efficiency to support real-time distributed monitoring.

## III. DESIGN

LightRanger operates through a coordinated, two-phase process between distributed measurement nodes and a central aggregation node, as illustrated in Fig. 5.

![](images/767320b8f1530d2eb357990e18e42543e2e417b0d3eca9b8753a8a2b97b6fab3.jpg)  
Fig. 5: LightRanger overview.

At the measurement node, LightRanger first performs Accuracy-Assurance Bucket Mapping. By observing the minimum and maximum bucket values within an epoch, it dynamically calculates uniform grouping intervals. This ensures buckets of similar magnitude are mapped together, preserving distribution structure. The maximum value within each group is recorded as its representative. Then, a Memory-Efficient Bitmap Construction scheme is applied, where the bitmap is adaptively pruned according to the available bandwidth budget.

At the aggregation node, LightRanger enables adaptive decompression and querying. For received data, it rapidly decodes group identifiers via bitwise operations. Queries are resolved by directly returning a group's representative maximum or by estimating values using group boundaries. Critically, if rows are discarded during compression, LightRanger leverages compact bitmap row distribution indicators to accurately reconstruct the missing data, ensuring high-precision recovery and maintaining end-to-end measurement fidelity.

## A. Flexible Compression at the Measurement Node

1) Accuracy-Assurance bucket mapping: During the measurement period, the distributed node performs the bucket update operation of the adopted sketch algorithm, and continuously updates the maximum bucket value m and minimum bucket value l. After that, the final obtained range of bucket value, i.e., $[l, m]$ , basically covers the entire value range of the current sketch. Suppose that the obtained sketch data contains W buckets, and $b_{i}$ is the value of the i-th bucket ( $i \in [1, W]$ ). Then, LightRanger divides the value range interval [l, m] into K continuous non-overlapping intervals $G_{1}, G_{2}, \ldots, G_{K}$ , where K is determined by the compression ratio r according to $\lceil K = W/r \rceil$ , and the step size of grouping is calculated as $\lfloor (m - l)/K \rfloor$ . By this way, each group interval is continuous and non-overlapping, ensuring that buckets with similar values are mapped to the same group, thus avoiding the error problem caused by traditional grouping.

LightRanger carries out three steps for bucket mapping:

① Quickly locating the target group to which $b_{i}$ belongs through group calculation. The time complexity of this mapping process is $\mathcal{O}(1)$ , ensuring rapid completion of group matching even when K takes a large value, and guaranteeing the efficiency of the mapping process.

② Comparing the $M_{k}$ of the target group with $b_{i}$ , where $M_{k}$ is the recorded maximum value of bucket in the k-th group. If $b_{i}$ is greater than the current $M_{k}$ , update $M_{k}$ to $b_{i}$ . This operation ensures that $M_{k}$ always represents the maximum value within the group, providing an accurate estimation basis for subsequent queries.

③ Recording the mapping relationship between the current bucket and the group using a temporary array.

![](images/0c47576d74d56fd5f703d9b8d7ffa6350d72ab6d3198dd35899fb4ebfce67f03.jpg)  
Fig. 6: Grouping and bucket mapping.

Fig. 6 presents an example to illustrate the specific process of bucket mapping. Assume that $l = 3$ , $m = 92$ , and $r = 3$ , then we have $K = 4$ and the grouping step size is 22. Thus, the original data is divided into four groups: $G_{1} = [3, 24]$ , $G_{2} = [25, 46]$ , $G_{3} = [47, 68]$ , and $G_{4} = [69, 92]$ . Next, the buckets $b_{1}$ to $b_{12}$ are mapped to $G_{1}$ to $G_{4}$ one by one. Meanwhile, the group number of each bucket is recorded to their own bucket for saving memory. After the group mapping is done, $M_{1}$ to $M_{4}$ is updated to 12, 45, NULL, and 92, respectively.

2) Memory-efficient bitmap construction: Upon completing bucket mapping, we design a bandwidth-adaptive bitmap construction strategy to accommodate diverse network bandwidth conditions, thereby striking a balance between transmission efficiency and query accuracy.

a) Unrestricted Network Bandwidth Scenario: In this case, we prioritize both memory efficiency and fidelity. Each group's $M_{k}$ and the constructed bitmap will be transmitted to the aggregation node. For example (see Fig. 7), $\{12, 45, NULL, 92\}$ , along with the original bitmap, are transmitted to the aggregation node. This method achieves the fastest compression speed and highest query accuracy because it preserves all data associated with group mapping. Consequently, the aggregation node can directly utilize the complete dataset for decompression and query processing, eliminating the need for additional estimation or compensation operations.

![](images/7e564d8984e7e566c6de288d9582f343f4483bd173e783ffca97f862a64c0006.jpg)  
Fig. 7: Bandwidth-unrestricted bitmap construction.

b) Restricted Network Bandwidth Scenario: In distributed monitoring architectures, backbone bandwidth is shared among user traffic, control planes, and management services. Consequently, transmitting measurement data must contend with these flows for limited capacity. To deliver sketches to the aggregation point within a strict delay bound, the size of compressed sketch data is inevitably constrained by the available network bandwidth. Assume that the available network bandwidth is B (measured in bits/second) and the transmission deadline of compressed sketch data is T (measured in seconds), then the maximum transmittable size of the compressed sketch data D is bounded by $D \leq \min(B \times T, W \times n/r)$ , wherein n is the number of bits contained by each bucket. LightRanger incorporates the following three core strategies to operate within this constraint.

Elimination of Empty Groups (EEG): Network measurement data typically follows a Zipf distribution, where a minority of flows carries the majority of the traffic volume, while most flows are small [14]. Consequently, in sketches, the vast majority of buckets hold minimal values, with only a few containing significant counts. This distribution leads to a critical inefficiency in LightRanger's grouping phase: many groups are mapped to no buckets at all. The representative values for these empty groups remain at their initialized defaults, providing no useful information and wasting transmission capacity. Therefore, identifying and eliminating these ineffective groups is essential. Pruning them directly reduces the size of the compressed sketch data, ensuring the transmittable data volume $D$ conforms to the stricter bound mentioned above and that bandwidth is used only for information-carrying data.

Fig. 8 illustrates LightRanger's procedure for EEG. The mechanism first filters and removes all groups whose recorded maximum value remains at the default initialization state, indicating they were never mapped to any bucket. The remaining valid groups are then compacted by assigning them new, continuous group indices to eliminate numbering gaps. Consequently, the mapping bitmap is constructed using these new indices, which are written into the bit positions corresponding to their original buckets. This process yields two key outputs for transmission: the compacted set of valid group maxima $M_{k'}$ and the bitmap of valid groups. At the aggregator, parsing an index in the bitmap now directly points to a valid maximum value, ensuring that bandwidth is used only for semantically meaningful data and that query resolution remains efficient.

![](images/7db7b9c5560e6c69246edabc1844579a2ef00228e15ad293be3b84dea2be42f7.jpg)  
Fig. 8: The procedures of EEG and BBR.

Boundary-based Representation (BBR): As shown in Fig. 8, if no empty groups exist or the transmission budget still cannot be met after EEG, LightRanger employs Boundary-based Representation as a fallback strategy. Instead of transmitting per-group maxima, BBR sends only the global value extrema, the minimum l and maximum m bucket values observed across the entire sketch, alongside the original bitmap. This eliminates the overhead of carrying individual group representatives, substantially reducing the payload size. This approach trades a bounded accuracy loss for guaranteed compliance with the transmission constraint. Decompression uses l and m to approximate values via uniform interpolation within groups, maintaining low computational complexity in both compression and reconstruction phases. BBR thus ensures operational feasibility under stringent bandwidth limits when finer-grained representations are infeasible.

Selective Bitmap Pruning (SBP): If neither EEG nor BBR can satisfy the bandwidth bound, LightRanger activates this stage (see Fig. 9). Let L and $L'$ denote the number of bitmap rows after EEG and BBR, respectively, and let $\Delta L$ and $\Delta L'$ be the number of rows that must be removed to meet the transmission budget. The pruning ratios $R_{1} = \Delta L / L$ and $R_{2} = \Delta L' / L'$ are computed, and the scheme with the smaller ratio is selected to minimize precision loss. To mitigate the indexing ambiguity introduced by row removal, SBP introduces a lightweight row-distribution indicator. During bitmap construction, each row maintains a counter cnt that accumulates “+1” for every “1” and “-1” for every “0”. A row’s dominant value is recorded in a flag f: f = 1 if cnt > 0, f = 0 if cnt < 0 (if cnt = 0, f is randomly assigned). Only the pruned bitmap and the compact array of f flags are transmitted. At the aggregation node, pruned rows are reconstructed by populating all bits with the corresponding dominant value f, enabling fast, low-error bitmap recovery through bitwise operations.

## B. Adaptive Decompression at the Aggregation Node

Upon receiving compressed data from measurement nodes, the aggregation node performs adaptive decompression and query processing (see Fig. 10). The received payload, which may include a combination of group-maxima sets ( $\{M_k\}$ or $\{M_k'\}$ ), global extrema ( $l, m$ ), a bitmap (possibly pruned), and row-distribution indicators, is first analyzed to determine its structure and integrity. When network bandwidth is sufficient, the process is streamlined: the aggregator directly parses group indices from the intact bitmap via $\mathcal{O}(1)$ bitwise operations and retrieves the corresponding group maximum $\{M_k\}$ as the query result. This mode preserves the original measurement fidelity without any estimation or reconstruction, enabling both high precision and real-time response.

![](images/acf8749691eaddae19abd88481071d706645dcd05431e68c4450b6b7d12ce94b.jpg)  
Fig. 9: The procedures of SBP.

Under bandwidth constraints, if the bitmap has been pruned, missing rows are reconstructed using the row-distribution indicators. First, each removed row is filled uniformly with its dominant bit value ("0" or "1") through lightweight bitwise operations. Second, group indices are decoded via bitwise parsing of the restored bitmap. Query resolution then adapts dynamically: if per-group maxima $\{M_k'\}$ are available, they are returned directly; if only global extrema $(l,m)$ are provided, the group step size is computed and the right boundary of the relevant group serves as the estimate.

![](images/66f52111d15d590a0fadf21bf04b85609d6ac939dbea8051cb43439035e9999b.jpg)  
Fig. 10: Aggregation node operations.

## C. Algorithms

The LightRanger architecture comprises two coordinated algorithms, whose key notation is summarized in Table I.

Algorithm 1 executes sketch compression at the measurement nodes, taking the S, r, B, T, W, l and m as inputs, and outputting $D_{c}$ . First, it runs initializations (Line 1), iterates over all buckets, calculates the group $k = \lfloor (b_{i} - l)/s \rfloor + 1$ that each bucket belongs to, updates $M_{k}$ , and records the group number of the bucket (Lines 2-4). Then, it generates the $P_{o}$ with L rows, and counts the number of valid groups $K'$ (Line 5). When bandwidth is unrestricted, it directly transmits the set of $\{M_{k}\}$ and the $P_{o}$ (Lines 6-8). When bandwidth is restricted, if $K' = K$ , it judges whether the data volume required for BBR meets the transmission limit: if yes, it transmits the global extrema and BBR bitmap; otherwise, it performs SBP on the BBR bitmap before transmission (Lines 9-13). If the number of valid groups is less than the initial number of groups, it first judges whether the data size after EEG complies with the transmission limit: if yes, it transmits the valid group maxima and EEG bitmap; otherwise, it runs the SBP on EEG and BBR, respectively, selecting the scheme with the smaller pruning ratio to minimize precision loss (Lines 14-25).

TABLE I: Key Notations and Parameters in LightRanger.

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td>S</td><td>The original sketch data.</td></tr><tr><td>r</td><td>The compression ratio (r≥1).</td></tr><tr><td>B</td><td>The available bandwidth (measured in bits/second).</td></tr><tr><td>T</td><td>The transmission deadline of compressed S (mea-sured in seconds).</td></tr><tr><td>W</td><td>The total number of buckets contained S.</td></tr><tr><td>l</td><td>The measured minimum bucket value in W.</td></tr><tr><td>m</td><td>The measured maximum bucket value in W.</td></tr><tr><td>bi</td><td>The value of the i-th bucket in W, i∈[1,W].</td></tr><tr><td>K</td><td>The number of groups before bucket mapping.</td></tr><tr><td>K&#x27;</td><td>The number of valid groups after bucket mapping.</td></tr><tr><td>s</td><td>The step size for grouping.</td></tr><tr><td>Mk</td><td>The maximum bucket value in the k-th group.</td></tr><tr><td>{Mk}</td><td>The set of group maxima.</td></tr><tr><td>L</td><td>The row count of the bitmap before pruning.</td></tr><tr><td>L&#x27;</td><td>The row count of the bitmap after pruning.</td></tr><tr><td>ΔL</td><td>The number of rows pruning for BBR().</td></tr><tr><td>ΔL&#x27;</td><td>The number of rows pruning for EEG().</td></tr><tr><td>n</td><td>The number of bits contained in each bucket.</td></tr><tr><td>D</td><td>The maximum transmittable size of the compressed sketch data.</td></tr><tr><td>Dc</td><td>The compressed data that is allowable to be trans-mitted to the aggregation node.</td></tr><tr><td>Po</td><td>The constructed bitmap after bucket mapping.</td></tr><tr><td>EEG()</td><td>The function of EEG.</td></tr><tr><td>BBR()</td><td>The function of BBR.</td></tr><tr><td>SBP()</td><td>The function of SBP.</td></tr><tr><td>PEEG</td><td>The constructed bitmap after EEG().</td></tr><tr><td>PBBR</td><td>The constructed bitmap after BBR().</td></tr><tr><td>I</td><td>The indicator generating after bitmap pruning.</td></tr></table>

Algorithm 2 implements decompression and query at the aggregation nodes, taking $D_{c}$ and query index $i$ as inputs, and outputting the query results. If $D_{c}$ is the SBP-pruned data, it first restores the pruned bitmap rows through indicators, then parses the group number (lines 1-6). Then, if $M_{k}$ is available, the algorithm directly returns $M_{k}$ (Lines 7-9). If $M_{k'}$ is available, $M_{k'}$ is directly returned as the query result (Lines 10-12). If $D_{c}$ is the BBR data, it re-executes dynamic uniform grouping ( $K = \lceil W / r \rceil$ , $s = \lfloor (m - l) / K \rfloor$ ), maps buckets to groups, and uses the right boundary of the group or derived maximum value as the query result (Lines 13-15).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Execution logic at the measurement node
Input: S, r, B, T, W, l, m
Output:  $D_{c}$ 
1 Initialize:  $K \leftarrow \lceil W/r \rceil$ ;  $s \leftarrow \lfloor (m - l)/K \rfloor$ ;  $M_{k} \leftarrow -\infty$ ;  $L \leftarrow \lceil \log_{2} K \rceil$ ;  $D \leftarrow min(B \times T, W \times n/r)$ ;
// Group mapping
2 for  $i \leftarrow 1$  to W do
3    $k \leftarrow \lfloor (b_{i} - l)/s \rfloor + 1$ ;  $M_{k} \leftarrow \max(M_{k}, b_{i})$ ;  $b_{i} \leftarrow k$ ;
4 end
// Bitmap construction
5 Generating  $P_{o}$  with L rows and obtaining  $K'$ ;
6 if B is unrestricted then
7    $D_{c} \leftarrow \{\{M_{k}\}, P_{o}\}$ ;
8 else
// No empty groups exist
9    if  $K' = K$  then
10    if  $2n + L \cdot \lceil \log_{2} K \rceil &lt; D$  then
11    $D_{c} \leftarrow \{l, m, P_{BBR}\}$ ;
12    else
13    $D_{c} \leftarrow \{l, m, SBP(P_{BBR}), I_{SBP}^{BBR}\}$ ;
14    end
15    // Empty groups exist
16    else
17    if  $K' \cdot n + L \cdot \lceil \log_{2} K' \rceil &lt; D$  then
18    $D_{c} \leftarrow \{\{M_{k'}\}, P_{EEG}\}$ ;
19    else if  $2n + L \cdot \lceil \log_{2} K \rceil &lt; D$  then
20    $D_{c} \leftarrow \{l, m, P_{BBR}\}$ ;
21    else
22    $ΔL' = \lfloor \frac{K' \cdot n + L' \cdot W - B}{W} \rfloor$ ;
23    $ΔL = \lfloor \frac{2n + L \cdot W - B}{W} \rfloor$ ;
24    if  $ΔL' / L' \leq ΔL / L$  then
25    $D_{c} \leftarrow \{\{M_{k'}\}, SBP(P_{EEG}), I_{SBP}^{EEG}\}$ ;
26    else
27    $D_{c} \leftarrow \{l, m, SBP(P_{BBR}), I_{SBP}^{BBR}\}$ ;
28    end
29    end
30    end
31 end
32 end
33 end
</div>

## IV. THEORETICAL ANALYSIS

In this section, we mathematically analyze the quantitative relationship between the original values of buckets and their compressed estimates. We derive the probability inequality in Lemma 1, which establishes the upper bound of the deviation between compressed estimates and original values, along with the corresponding probability guarantee.

Lemma 1. For the original value $b_{i}$ of any bucket i, its

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Execution logic at the aggregation node
Input: Received data $D_c$; Query bucket index $i$;
Output: Query result for bucket $i$;
1 if I is available then
2 | Reconstructing bitmap based on the indicator;
3 else
4 | $k \leftarrow$ The value of the $i$-th column from the bitmap;
5 end
6 if $M_k$ is available then
7 | return $M_k$;
8 else if $M_{k'}$ is available then
9 | return $M_{k'}$;
10 else
11 | $K \leftarrow \lceil W/r \rceil$; return $k = K?m : l + k \cdot \frac{m - l}{K}$;
12 end
</div>

$$
\hat {b} _ {i}
$$

$$
\operatorname * {P r} \left(\hat {b} _ {i} - b _ {i} \geq \epsilon \| \vec {f} \| _ {1}\right) \leq 1 - \left(1 - \frac {K l + m - l}{K (b _ {i} + \epsilon \| \vec {f} \| _ {1})}\right) ^ {m _ {j} - 1}.\tag{1}
$$

Proof: Let the bucket array of the original sketch in a distributed node be $B = [b_{1}, b_{2}, \ldots, b_{i}]$ (with W as the total number of buckets and $b_{i}$ denoting the original value of the i-th bucket, where $i \in [1, W]$ ). In the compression mechanism, the initial number of groups $K = \lceil W/r \rceil$ is determined by the compression ratio r, and after invalid group optimization, the number of effective groups is $K'$ ( $K' \leq K$ ). For notation, we define $\vec{f} = [b_{1}, b_{2}, \ldots, b_{i}]$ as the original bucket value vector, whose $L_{1}$ -norm $\|\vec{f}\|_{1} = \sum_{i=1}^{W} b_{i}$ represents the total size of the data streams; $M_{j}$ as the maximum value of the j-th effective group, which contains $m_{j}$ buckets (with $\sum_{j=1}^{K'} m_{j} = W$ ); $\hat{b}_{i}$ as the estimated value of the i-th bucket after compression (equal to $M_{j}$ of the effective group that the i-th bucket belongs to); and $\epsilon > 0$ as the allowed relative error threshold, with the goal of deriving the upper bound of $\Pr(\hat{b}_{i} - b_{i} \geq \epsilon \| \vec{f} \|_{1})$ . Then, we have

$$
\leq 1 - \operatorname * {P r} \left(M _ {j} - b _ {i} <   \epsilon \| \vec {f} \| _ {1}\right)
$$

$$
= 1 - \operatorname * {P r} \left(\max \left\{b _ {i}, b _ {1}, \dots , b _ {m _ {j} - 1} \right\} <   b _ {i} + \epsilon \| \vec {f} \| _ {1}\right)
$$

$$
= 1 - \operatorname * {P r} \left(b _ {i} <   b _ {i} + \epsilon \| \vec {f} \| _ {1}\right) \prod_ {t = 1} ^ {m _ {j} - 1} \operatorname * {P r} \left(b _ {t} <   b _ {i} + \epsilon \| \vec {f} \| _ {1}\right)
$$

$$
\left(b _ {i} <   b _ {i} + \epsilon \| \vec {f} \| _ {1}\right) = 1\tag{2}
$$

$$
\operatorname * {P r} \left(\hat {b} _ {i} - b _ {i} \geq \epsilon \| \vec {f} \| _ {1}\right) \leq 1 - \prod_ {t = 1} ^ {m _ {j} - 1} \operatorname * {P r} \left(b _ {t} <   b _ {i} + \epsilon \| \vec {f} \| _ {1}\right).\tag{3}
$$

According to the Markov inequality, for non-negative $b_{t}$ :

![](images/ca96aae964456cc701c67fb0fa9faa6aa053c499ccce8c47b67e4949972d13bd.jpg)  
(a) CM Sketch

![](images/ce31fcee2123bcd85be3a8f9e81c3c04b5d565c413d63222b61a12528ecec130.jpg)  
(b) CU Sketch

![](images/e3be54a07b1f6288c50e59362dcc0dc97c50c4805d5a92c206dad8a4d1bf4b73.jpg)  
(c) CMM Sketch

![](images/1606fd7be769db85e7bb1ca8a1d49c42d9921664bdbb90777be1017664d27257.jpg)  
(d) CSM Sketch  
Fig. 11: Low compression ratio.

![](images/dadcd88c4aa22fd7f07e9c5a277eb7e7ce197a57fd604900fa7572a6de0a04bd.jpg)  
(a) CM Sketch

![](images/f367385b695eaa91641da685f8b7b7a5f1b59f5fb683b90c91959abdaae47183.jpg)  
(b) CU Sketch

![](images/1e994c530bec3f90baa765780f31fc24c11fc46692d44e2aa61a1aa5a3069715.jpg)  
(c) CMM Sketch

![](images/29afd7f6d99920b64f99d4102505821610abbdabcfaccea3c015125293f88906.jpg)  
(d) CSM Sketch  
Fig. 12: Medium compression ratio.

![](images/0cebeb348540159c5e98708b2d3d9f057fe94b75ddb6011bd43fa67a8f87514d.jpg)  
(a) CM Sketch

![](images/1d5a6e2e8a4664107d468a9221b441121d7fdb35d8deffea13b3bd938c2f2a95.jpg)  
(b) CU Sketch

![](images/7e2c031d70a767e9190c889c00d0a99f8e4814f5e34f2212f963694303f9b1cc.jpg)  
(c) CMM Sketch

![](images/605f5d2d46860dd1a3be4414620d48be54f9c22f7fcdf029efe0c93d442ff8f3.jpg)  
(d) CSM Sketch  
Fig. 13: High compression ratio.

$$
\begin{array}{c} \operatorname * {P r} \left(b _ {t} <   b _ {i} + \epsilon \| \vec {f} \| _ {1}\right) \geq 1 - \frac {\mathbb {E} (b _ {t})}{b _ {i} + \epsilon \| \vec {f} \| _ {1}} \\ \geq 1 - \frac {l + \frac {m - l}{K}}{b _ {i} + \epsilon \| \vec {f} \| _ {1}}. \end{array}\tag{4}
$$

Substituting Equation (3) into Equation (2), we obtain:

$$
\begin{array}{l} \operatorname * {P r} \left(\hat {b} _ {i} - b _ {i} \geq \epsilon \| \vec {f} \| _ {1}\right) \leq 1 - \prod_ {t = 1} ^ {m _ {j} - 1} \left(1 - \frac {l + \frac {m - l}{K}}{b _ {i} + \epsilon \| \vec {f} \| _ {1}}\right) \\ \leq 1 - \prod_ {t = 1} ^ {m _ {j} - 1} \left(1 - \frac {K l + m - l}{K (b _ {i} + \epsilon \| \vec {f} \| _ {1})}\right) \\ \leq 1 - \left(1 - \frac {K l + m - l}{K (b _ {i} + \epsilon \| \vec {f} \| _ {1})}\right) ^ {m _ {j} - 1}. \end{array} \tag {7}\tag{5}
$$

## V. EVALUATION

## A. Experimental Setup

This section covers diverse scenarios and adopts the experimental platform configuration, compared methods and compression ratios from the Section II-C to ensure consistency. We select four types of representative network traffic datasets, including three real-world datasets and one synthetic dataset: CAIDA $[15]$ consists of public traffic traces collected from the Equinix-Chicago monitor in 2019. MAWI $[17]$ and Webdocs $[18]$ are datasets of approximately 2.1GB and 1.5GB, respectively, collected from their corresponding sources. The synthetic dataset is Zipf, which simulates heavy-tailed distribution traffic by Web Polygraph with a skewness of 0.3 $[19]$ . All datasets are preprocessed into standardized data stream, and we extract flow frequencies or byte counts as bucket values. We adopt four sketches to adapt to different tasks and scenarios, i.e., CM sketch $[16]$ , CMM Sketch $[20]$ , CU Sketch $[21]$ , and CSM Sketch $[22]$ .

![](images/945f3cc39e8603b9cea08649bd1c472b9ee6902bf94690740bf6b7070a04be9d.jpg)  
(a) CM Sketch.

![](images/0818b8dce8a5ad2f0c098a2d8192c0942cc5011c2ddb79bb604ac745492afc3a.jpg)  
(b) CMM Sketch.

![](images/0b459536cb3325a8ee00a5993633ac806e4fea6d6d7781804899dd93940127f8.jpg)  
(c) CU Sketch.

![](images/967d761c995171547c09e40b00e058b2937d24ede84fcad6c002f1fab44863ca.jpg)  
(d) CM Sketch.

![](images/be13dd5eadee56aa681ef0768c5ba1b2ea37816882749099d40d7d551f4c3d78.jpg)  
(e) CMM Sketch.

![](images/ae47277cc1cbe337f9d13d1936a7d240372448de4e568bff9f64de446a5b7aee.jpg)  
(f) CU Sketch.

Fig. 14: Performance of each dataset under different Sketches  
![](images/4c72fbbfc3be0adaa6d6c8e52ea4306984923207d224ee058ca980bdbbdd133d.jpg)  
Transfer Limit (MB)  
Fig. 15: Performance under different transmission constraints

## B. Experimental Results

1) Performance Verification with Multiple Compression Ratios on CAIDA Dataset: Based on the CAIDA dataset (a real Internet backbone trace containing numerous large flows and a highly skewed value distribution), we verify the adaptability of LightRanger on four sketch structures under low, medium, and high compression ratios. From Fig. 11 to Fig. 13, LightRanger achieves an excellent balance between accuracy and speed. Compared with Hokusai and Elastic, its ARE is significantly lower, with a maximum reduction of $97.94\%$ over Hokusai and $92.60\%$ over Elastic. The reason is that such methods indiscriminately merge high-value and low-value buckets, resulting in large and unbounded estimation errors. Notably, even at high compression ratios, LightRanger still keeps the average relative error at a low level, with a maximum reduction of $93.04\%$ over clustering methods, while the compression time of clustering methods is up to about $37 \times$ that of LightRanger. This advantage stems from LightRanger's use of global extrema to dynamically generate uniform intervals and group buckets with similar values with $O(1)$ mapping complexity, thus avoiding the large errors caused by traditional grouping. Although LightRanger's compression time is slightly higher than that of Hokusai and Elastic, it still remains at the microsecond-to-millisecond level.

2) Applicability Verification Across Multiple Datasets: We conduct cross-dataset performance evaluations under various compression ratios. Due to space limitations, this paper only presents experimental results for three typical sketches at a compression ratio of 3, as shown in Fig. 14. LightRanger exhibits stable and superior overall performance on the MAWI, Zipf, and Webdocs datasets. In terms of accuracy, LightRanger achieves the lowest ARE on CM, CU, and CMM sketches, with particularly prominent advantages in the long-tailed Zipf scenario (see Figs. 14a-14c). Notably, the internal value variations in the MAWI and Webdocs datasets are small, leading to relatively good performance of Elastic in such scenarios. In contrast, Hokusai adopts cumulative compression and still incurs significant errors even in scenarios with small data differences. In terms of latency, LightRanger's CT is stable and controllable, only slightly higher than that of traditional grouping-based methods. In sharp contrast, IC-3 and DP exhibit extremely high compression latency, far exceeding that of LightRanger (see Figs. 14d-14f), making them difficult to meet the requirements of real-time measurement.

3) Adaptive Performance Under Transmission Limits: LightRanger achieves a dynamic balance among bandwidth, accuracy, and speed under 0-5 MB transmission limits. In Fig. 15, under the extreme constraint of 1 MB payload and 10 MB original sketch, LightRanger removes empty groups via EEG, retains high-order indices, and recovers low-order indices via SBP, ensuring controllable ARE and low distortion. EEG eliminates empty groups caused by Zipf distribution without information loss. BBR reduces payload with bounded accuracy loss. SBP reconstructs pruned bits to minimize error. As limits relax, LightRanger dynamically adapts its strategy. Overall, ARE decreases steadily while CT remains at the microsecond-to-millisecond level. When bandwidth is sufficient, LightRanger transmits full data without pruning, achieving near-optimal ARE with negligible overhead. This hierarchical adaptability makes LightRanger more efficient than conventional grouping and clustering methods.

## VI. RELATED WORK

Existing sketch compression approaches fall into several categories [6]–[8], [23], [24].

Group-aggregation schemes such as Hokusai [7] and Elastic [6] merge adjacent counters via sum or max operations. They are fast and storage-efficient but ignore per-counter variance, leading to large errors under skewed distributions. Clustering-based methods (e.g., Cluster-Reduce [8]) group counters by similarity to improve accuracy, but incur high computational overhead and extra metadata, limiting real-time applicability. Structure-adaptive techniques (e.g., TreeSensing [23]) exploit data sparsity or historical patterns for better compression, yet introduce either implementation complexity or limited adaptability to dynamic streams. Lossless compression ensures zero error but suffers from low compression ratios and high CPU cost, while hierarchical sketches (e.g., Pyramid Sketch [24]) are designed for query efficiency rather than transmission compression.

In contrast, LightRanger uses only real-time extrema for dynamic grouping and lightweight bitmap encoding, while supporting fast queries and broad sketch compatibility.

## VII. CONCLUSION

Sketch compression is essential for efficient distributed stream monitoring, yet existing methods fail to balance accuracy with efficiency. We propose LightRanger, a real-time, history-agnostic compression scheme using dynamic value-range grouping and adaptive bitmap pruning. Evaluation on diverse datasets and sketch types shows our approach achieves obvious accuracy improvement compared with mainstream compression algorithms while maintaining millisecond-scale latency and broad compatibility. Future work will explore hardware acceleration and self-adaptive mechanisms for dynamic network conditions.

## ACKNOWLEDGEMENT

This work is supported in part by the Key Scientific Research Project of Hunan Provincial Department of Education under Grant 25A0634; in part by the National Natural Science Foundation of China under Grant 62372068; in part by the Hunan Province Natural Science Foundation of China under Grant 2024JJ5050 and Grant 2025JJ50371; in part by the Hunan Province Key Laboratory of Industrial Internet Technology and Security under Grant 2019TP1011.

## REFERENCES

[1] Y. Li, J. Huang, C. Wu, X. Zhu, and J. Wang, "SwitchTop-k: Scaling top-k compression on programmable switches," in Proc. ACM SIGKDD, 2025, pp. 1612-1622.

[2] Y. Zhao, J. Huang, X. Su, W. Li, X. Li, Y. Liu, J. Xie, Q. Su, J. Ye, W. Jiang, and J. Wang, “Cardinality is Not Enough: Super Host Detection via Segmented Cardinality Estimation,” in Proc. ACM WWW, 2026.

[3] W. Li and P. Patras, “Stable-Sketch: A Versatile Sketch for Accurate, Fast, Web-Scale Data Stream Processing,” in Proc. ACM WWW, 2024, pp. 1890-1901.

[4] W. Li and P. Patras, "P-Sketch: A Fast and Accurate Sketch for Persistent Item Lookup," IEEE/ACM Transactions on Networking (TON), vol. 32, no. 5, pp. 2245-2258, Oct. 2024.

[5] Y. Zhang, Z. Liu, R. Wang, T. Yang, J. Li, R. Miao, P. Liu, and R. Zhang, “CocoSketch: High-performance Sketch-based Measurement over Arbitrary Partial Key Query,” in Proc. ACM SIGCOMM, 2021, pp. 207-222.

[6] T. Yang, J. Jiang, P. Liu, Q. Huang, J. Gong, Y. Zhou, R. Miao, X. Li, and S. Uhlig, “Elastic Sketch: Adaptive and Fast Network-wide Measurements,” in Proc. ACM SIGCOMM, 2018, pp. 561-575.

[7] S. Matusevych, A. J. Smola, and A. Ahmed, “Hokusai-Sketching Streams in Real Time,” in Proc. UAI, 2012, pp. 594-603.

[8] Y. Zhao, Z. Zhong, Y. Li, Y. Zhou, Y. Zhu, L. Chen, Y. Wang, and T. Yang, “Cluster-Reduce: Compressing Sketches for Distributed Data Streams,” in Proc. ACM SIGKDD, 2021, pp. 2316-2326.

[9] Z. Liu, A. Manousis, G. Vorsanger, V. Sekar, and V. Braverman, “One Sketch to Rule Them All: Rethinking Network Flow Monitoring with UnivMon,” in Proc. ACM SIGCOMM, 2016, pp. 101-114.

[10] J. Huang, W. Zhang, Y. Li, L. Li, Z. Li, J. Ye, and J. Wang, "ChainSketch: An Efficient and Accurate Sketch for Heavy Flow Detection," IEEE/ACM Transactions on Networking (TON), vol. 31, no. 6, pp. 2812-2824, Dec. 2023.

[11] S. Narayana, A. Sivaraman, V. Nathan, P. Goyal, V. Arun, M. Alizadeh, V. Jeyakumar, and C. Kim, “Language-directed hardware design for network performance monitoring,” in Proc. ACM SIGCOMM, 2017, pp. 114.

[12] J. Hu, H. Q. Shen, Y. Liu, and J. Wang, "DMA-Sketch: A Fast and Accurate Sketch for Priority-Oriented Data Stream Processing," in Proc. IEEE/ACM IWQoS, 2025, pp. 1-6.

[13] J. Wang, C. Y. Zhu, and J. Hu, "A High-Accuracy Sketch for Measuring Low-Entropy Flows in Distributed AI Training," in Proc. ACM ICPP, 2025, pp. 53-62.

[14] Z. Fan, Y. Zhang, T. Yang, M. Yan, G. Wen, Y. Wu, H. Li, and B. Cui, "PeriodicSketch: Finding Periodic Items in Data Streams," in Proc. IEEE ICDE, 2022, pp. 96-109.

[15] The CAIDA Internet Traces. http://www.caida.org/data/overview/.

[16] G. Cormode and S. Muthukrishnan, “An Improved Data Stream Summary: the Count-Min Sketch and Its Applications,” Journal of Algorithms, vol. 55, no. 1, pp. 58-75, 2005.

[17] MAWI Working Group Traffic Archive. http://mawi.wide.ad.jp/mawi/.
[18] Real-life transactional dataset. http://fimi.ua.ac.be/data/.

[19] A. Rousskov and D. Wessels, “High-performance benchmarking with Web Polygraph,” Software: Practice and Experience, vol. 34, no. 2, pp. 187-211, 2004.

[20] C. Ma, H. Wang, O. Odegbile, and S. Chen, "Noise Measurement and Removal for Data Streaming Algorithms with Network Applications," in Proc. IEEE IFIP Networking, 2021, pp. 1-9.

[21] C. Estan and G. Varghese, “New Directions in Traffic Measurement and Accounting: Focusing on the Elephants, Ignoring the Mice,” ACM Transactions on Computer Systems (TOCS), vol. 21, no. 3, pp. 270-313, 2003.

[22] T. Li, S. Chen, and Y. Ling, "Per-flow traffic measurement through randomized counter sharing," IEEE/ACM Transactions on Networking (TON), vol. 20, no. 5, pp. 1622-1634, 2012.

[23] Z. Liu, Y. Zhang, Y. Zhu, R. Zhang, T. Yang, K. Xie, S. Wang, T. Li, and B. Cui, "TreeSensing: Linearly Compressing Sketches with Flexibility," in Proc. ACM SIGMOD, 2023, pp. 1-28.

[24] T. Yang, Y. Zhou, H. Jin, S. Chen, and X. Li, "Pyramid Sketch: A Sketch Framework for Frequency Estimation of Data Streams," in Proc. VLDB, 2017, pp. 1442-1453.