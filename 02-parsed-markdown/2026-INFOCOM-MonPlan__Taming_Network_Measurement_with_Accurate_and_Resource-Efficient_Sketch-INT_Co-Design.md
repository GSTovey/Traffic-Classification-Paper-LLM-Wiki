# MonPlan: Taming Network Measurement with Accurate and Resource-Efficient Sketch-INT Co-Design

Xiang Chen<sup>1</sup>, Linying Zheng<sup>1</sup>, Longlong Zhu<sup>1</sup>, Zedi Chen<sup>1</sup>, Qing Shu<sup>1</sup>, Jialu Tian<sup>1</sup>, Siqi Dong<sup>1</sup>, Qun Huang<sup>2</sup>, Jianshan Zhang<sup>3</sup>, Xuan Liu<sup>4</sup>, Haifeng Zhou<sup>1</sup>, Hongyan Liu<sup>5</sup>, Dong Zhang<sup>5</sup>, Chunming Wu<sup>1</sup> <sup>1</sup>Zhejiang University <sup>2</sup>Peking University <sup>3</sup>Minjiang University <sup>4</sup>Yangzhou University <sup>5</sup>Fuzhou University

Abstract—Network measurement is now a basic building block that supports network management applications to identify realtime events by measuring both large and small flows. However, existing techniques face the trade-off between high accuracy and resource efficiency: sketch-based techniques enjoy high accuracy and low resource consumption when measuring large flows but drop accuracy for small flows; in-band network telemetry (INT) measures every flow at the cost of high resource consumption. In this paper, we present MonPlan, a framework that utilizes both sketches and INT to measure large and small flows, respectively, offering both high measurement accuracy and resource efficiency. Unlike existing studies, our co-design is driven by two theoretical optimizations: (1) MonPlan adopts the near-optimal Lagrangian relaxation to solve the NP-hard selection of measurement points to deploy sketches and INT even when the routing information is unknown. (2) MonPlan estimates the worst-case rates of collecting measurement data. Its estimates support reinforcement learning to select paths without network congestions. We realize MonPlan on 12.8 Tbps programmable switches. With large-scale real-world topologies and nine network management applications, MonPlan provides 23∼95% higher accuracy and retains resource efficiency when compared with five types of existing techniques.

## I. INTRODUCTION

Network measurement measures traffic statistics such as perflow packet counts in switches and periodically collects these measurement data to the control plane. The control plane offers these data to network management applications that identify the events of their interest and making corresponding decisions [1].

In particular, both large flows (i.e., the flows that comprise a lot of packets) and small flows are essential to measurement: volumetric applications that query the sizes of each flow, e.g., heavy hitter and superspreader detection [2, 3], make decisions on large flows, while other types of applications, including flow size distribution [4] and congestion control [5, 6], address the importance of accurately measuring small flows.

However, existing measurement techniques face the dilemma of achieving both high accuracy and resource efficiency when measuring large and small flows. More precisely, the literature mainly exploits sketches and in-band network telemetry (INT). For sketches [7, 8, 3, 9, 10, 11, 12, 13, 14], they achieve accurate measurement for large flows via compact data structures. While sketches are resource-efficient, they exhibit low accuracy when measuring small flows due to the short of switch memory. For INT-based techniques [6, 5, 15, 16, 17], they record statistics within the INT headers of each packet and collect these headers at the egress of networks. Although their per-packet monitoring improves accuracy, it requires non-trivial bandwidth and control plane resources to handle large volumes of INT data.

Recent hybrid systems combine both sketches and INT [18, 19] but they still fall short. Typical examples include SketchINT [18] that builds sketches at the control plane based on collected INT data to rapidly react to flow queries while LightGuardian [19] that inserts sketch data into INT headers to achieve efficient measurement data collection. However, SketchINT still inherits the cost of INT while both SketchINT and LightGuardian suffer from low accuracy for small flows due to the nature of sketches.

Although recent studies attempt to break the above dilemma, they come at additional cost. Some of them propose sophisticated sketches such as elastic sketches [8] and pyramid sketches [20] that distinguish the measurement of small flows from large flows to mitigate the errors originated from hashing collisions. However, they involve complex data structures and operations, which hinder their hardware implementation, and also require time-consuming parameter tuning. Also, a lot of optimizations reduce INT overheads via the strategies such as path planning [16] or probabilistic updating [5]. Nevertheless, given the large volume of large flows, massive packets collectively force INT to generate a high-speed stream of INT headers, which brings non-trivial pressure to the control plane.

Here, we aim to answer the following question: how to build accurate and resource-efficient measurement towards both large and small flows? Our answer is MonPlan, which is an accurate and resource-efficient measurement framework. Our core idea originates from our observation: sketches and INT techniques are complementary to each other. More precisely, sketches trade their accuracy of measuring small flows for resource efficiency at scale, while INT techniques trade their resource efficiency for full accuracy of measuring every flow. Hence, their advantages and limitations lead to the possible match: for traffic in modern networks, which is considered skewed (i.e., most packets come from a few large flows) [21, 11, 22, 23, 8], MonPlan leverages sketches to measure large flows while using INT techniques to measure small flows: sketches offer high accuracy and resource efficiency for large flows while the small number of packets in small flows helps INT limit resource consumption and maintain high accuracy by avoiding congestion and data loss.

While this concept is intuitive, combining sketches with INT faces two optimization challenges: C1: where to install sketches and INT to measure as many flows as possible when routing information is unknown, and C2: how to prevent measurement data collection from congesting network paths and affecting normal traffic still remain hard optimization problems. Ignoring C1 leads to high measurement errors due to the miss of massive flows while neglecting C2 results in severe measurement data loss during traffic bursts, e.g., existing hybrid systems [18, 19] that incorporate both sketches and INT ignore these challenges and suffer from accuracy and efficiency loss (§VI). To address the challenges, MonPlan presents two optimizations, including measurement point selection that yields near-optimal decisions under unknown routing information, and congestion-free data collection that profiles worst-case estimates to determine lossfree decisions. The proposed optimizations enable MonPlan to achieve both high accuracy and resource efficiency in practice. Contributions. We summarize our contributions as follows.

• We exploit the opportunity of combining sketches and INT by proposing MonPlan, a framework that adopts sketches to measure large flows while using INT to measure small flows, enabling accurate and resource-efficient measurements (§III).

• In response to the challenges of lacking routing knowledge and NP hardness, MonPlan addresses the measurement point selection problem with Lagrangian relaxation and guarantees near-optimal decisions with bounded optimality gaps (§IV).

• MonPlan integrates the worst-case estimations, which model sending rates of measurement data with bursts, into reinforcement learning that dynamically selects paths to transfer data from switches to the control plane without congestions (§V).

• We have implemented MonPlan atop our testbed that comprises 12.8 Tbps programmable switches [24]. Testbed experiments with large-scale real-world topologies and nine network management applications show that MonPlan provides 23∼95% higher accuracy while retaining resource efficiency when compared with five types of existing techniques (§VI).

## II. BACKGROUND AND MOTIVATION

## A. Our Scope: Network Measurement

We first illustrate our scope in this paper. We follow existing studies [14, 25, 10] to consider a general architecture of network measurement comprising two planes. In the data plane, switches execute sketches and INT techniques to collect traffic statistics to a cluster of servers that collectively act as the control plane. The control plane runs network management applications that query statistics to identify network events and make decisions. We define relevant terms without loss of generality [26, 27]:

• Each packet can be regarded as a tuple of header fields (e.g., IP) and metadata (e.g., packet size and location traversed).

• Each flow groups the packets that share the same set of header fields and metadata, e.g., the same source IP address.

• Traffic statistics, or per-flow statistics, correspond to the flow attributes of interest, e.g., per-flow packet counts.

## B. Sketches and Limitations

Sketches are the approximate algorithms that provide nearoptimal accuracy guarantees to the measurement of large flows. Their resource consumption is below a limited budget, making them compatible with resource-constrained switches. Numerous studies [7, 8, 3, 9, 10, 11, 12, 13, 14] have shown that sketches provide better accuracy-resource tradeoffs for large flows when compared with sampling-based techniques.

Limitation 1 (L1): Sketches can hardly provide high accuracy for small flows. Sketches can only use a few memory in their data structures due to switch resource constraints. As a result, the data of large flows and small flows easily collide, resulting in measurement errors. In particular, the measurement of small flows is extremely sensitive to such errors because these flows have very few packets and may be missed entirely or their small counts may be overestimated due to hash collisions.

We validate our claim with testbed experiments. We consider five sketches and employ them for the application of per-flow packet counting, i.e., the count-min sketch (CM) [28], the count sketch (CS) [29], the elastic sketch (ES) [8], SketchLearn (SL) [9], and UnivMon (UM) [10]. We consider the de-facto standard traffic traces, CAIDA [22], and partition them into two-second intervals, each containing 100 K flows. Then for each sketch, we allocate 10 MB to its data structures because this configuration approximates the maximum memory capacity per switch [30]. We measure the ratio of flows with < 10% errors in each sketch. Due to space limitations, we report numerical results: all ratios are lower than 50% because most small flows suffer from nontrivial errors due to memory shortage.

Some recent studies have been proposed to tackle the above issue. For example, NZE-sketch [11] leverages the theories of compressive sensing to design sketches to approximately record traffic data in switches, and recover original data in the control plane. Moreover, learning-based sketches such as TalentSketch [31] leverage machine learning models to identify which flows suffer from low measurement accuracy and update sketch data structures in subsequent measurements. However, they exhibit similar issues. First, they need specific sketch design to enforce their optimizations, losing the generality of supporting different types of sketches or network management applications. Second, their recovery or updating strategies require tens of seconds, making them unsuitable for a lot of scenarios in which measurements should be made within a few milliseconds. For example, DDoS detection addresses sub-millisecond detection time [32].

## C. In-Band Network Telemetry (INT) and Limitations

The core idea of INT is simple yet effective. For each packet, INT orders every switch that the packet traverses to piggyback the information required for measurement onto the packet’s INT header. At the egress switch, where packets leave the network, their INT headers are extracted and emitted to the control plane for further analysis. Thus, INT preserves full accuracy for every flow, especially for small flows.

Limitation 2 (L2): INT can bring significant network resource overheads. Since INT corresponds to per-packet monitoring, it inevitably brings significant overheads to both network bandwidth (for transferring INT headers) and control plane resources (for processing INT headers) given massive packet number. In theory, according to the INT protocol [33], each switch will add a 12-byte INT header to each packet while the total number of INT headers equals the number of hops traversed by the packet. Given that modern networks transfer Tbps-level traffic, the total number of packets per second exceeds 10<sup>9</sup>, corresponding to the number of INT headers to be emitted simultaneously. Hence, although 12 bytes seem to be small, the accumulation of more than 10<sup>9</sup> INT headers becomes significant and unacceptable.

![](images/c484e386a2691ca409a20a310078f3200bf9a70f1496b9d4bb3e4b4bb8c68d89.jpg)  
Fig. 1: MonPlan overview.

To date, many optimizations have been proposed to optimize INT overheads. First, some of them rely on sampling and only invoke INT for sampled packets [34, 35, 36, 5]. Nevertheless, sampling degrades accuracy as it ignores many packets, especially for small flows with a few packets. Also, the control plane requires a long time for result convergence. Next, INT-path [16] sends probes to determine the minimum set of non-overlapped paths that INT must measure. But its per-packet monitoring still suffers from high overheads. Second, some approaches propose to simplify INT information on each packet [5, 19, 6]. PINT [5] reduces INT metadata via sampling-based global hashing and distributed encoding. But it inherits the issues of sampling.

## D. Limitations of Hybrid Sketch+INT Solutions

Two recent techniques provide hybrid solutions that combine sketches and INT. First, SketchINT [18] activates INT at data plane switches while leveraging sketches at the control plane to aggregate INT data and simplify subsequent analysis. However, due to its base of INT, it inherits L2. Also, its use of sketches trades the accuracy of small flows for control plane efficiency, leading to L1. Second, LightGuardian [19] uses small sketches to encode INT data in each packet in a compact manner. Hence, it addresses L2 because it only requires a few packets to deliver a small amount of sketch data via INT. But given the nature of sketches, it inevitably loses accuracy for small flows, i.e., L1.

## III. OVERVIEW OF MONPLAN

Goals. We aim to achieve two goals of network measurement.

• G1: High accuracy, i.e., measuring large flows and small flows accurately (addressing L1, §II-B).

• G2: Resource efficiency, i.e., avoiding high resource overheads in measurement data collection (addressing L2, §II-C). Key idea. We observe that sketches and INT complement each other. More precisely, sketches exhibit both high accuracy and resource efficiency for large flows, but they fall short for small flows; INT can provide high accuracy for both large and small flows, but they come at the cost of high resource consumption.

In this context, we can use sketches to measure large flows while using INT to measure small flows. Specifically, before a flow becomes a large flow, its packets will be measured by both sketches and INT. Once it is identified by sketches as a large flow, it will be only recorded by sketches. Doing so can achieve both high accuracy and resource efficiency. In detail, traffic in modern networks is skewed [21, 11, 22, 23, 8]. Thus, most packets come from large flows, which are accurately and efficiently measured by sketches. For other packets from small flows, they are measured by INT, ensuring their full accuracy. Also, their number is small, limiting INT’s resource consumption. Hence, both G1 and G2 can be achieved simultaneously. Challenges. However, while our key idea is technically sound, realizing it faces two optimization challenges.

• C1: Measurement point selection with incomplete knowledge. Traffic routing details are usually unknown in advance. As such, selecting measurement points (i.e., switches that run sketches and INT) is non-trivial. First, the uncertainty of routing paths may result in over-provisioning of measurement points, increasing deployment overheads. Second, measurement points should be close to the control plane. Otherwise, measurement data collection may suffer from high latency. In summary, without routing information, selecting points with both high coverage and low collection latency is NP-hard.

• C2: Congestion-free measurement data collection under bursts. Measurement data from sketches and INT generates data streams that may saturate network paths connecting measurement points with the control plane. Thus, this challenge stems from the need to prevent the streams of measurement data from causing congestion during collection. For example, when thousands of incoming flows simultaneously activate INT at switches, the resulting measurement data traffic can overwhelm 100-Gbps paths in milliseconds. Thus, avoiding congestion requires complicated modeling of worst-case collection rates to prevent collisions with normal traffic.

Design. In response, we design MonPlan, a framework that codesigns sketches and INT to collectively achieve high accuracy (G1) and resource efficiency (G2). To address the challenges, MonPlan embraces two-pronged optimizations.

• Near-optimal measurement point selection. Given a network and a set of orientation-destination (OD) pairs, each of which represents the ingress and egress of a specific flow, MonPlan chooses enough switches to place sketches and INT. It aims at maximizing the coverage of measured flows and minimizing the distance between the switches where flows are measured and the control plane where traffic statistics are collected and analyzed. Next, it formulates such an optimization as a multiobjective facility location problem and leverages Lagrangian relaxation to obtain near-optimal decisions (addressing C1).

• Congestion-free measurement data collection. Switches collectively report high-speed streams of measurement data to the control plane via normal network paths. Therefore, these streams may be collided with normal traffic, causing network congestion and significant data loss. To prevent congestions, MonPlan automatically profiles the maximum possible rate of sending measurement data from every switch to the control plane. According to profiling results, it decides which paths to transfer data while avoiding congestion (addressing C2).

## Architecture. In Figure 2, MonPlan uses a four-step workflow:

1 Administrators submit the sketches and INT techniques they plan to use to MonPlan. As a general framework, MonPlan supports arbitrary types of sketches and INT techniques.

2 Without precise information, MonPlan solves the selection of measurement points via a Lagrangian relaxation algorithm that yields near-optimal decisions within polynomial time.

3 MonPlan performs sketches and INT atop selected switches. Each flow will be first measured by sketches. If it is identified as a large flow, its data is approximately recorded by sketches. Otherwise, its data is piggybacked on its headers via INT.

4 MonPlan selects network paths to transfer measurement data with the goal of avoiding congestion with normal traffic. The control plane receives data, which is input to applications for subsequent network management.

## IV. NEAR-OPTIMAL MEASUREMENT POINT SELECTION

Overview. The measurement point selection problem aims to select programmable switches in the network to deploy sketches and INT. It has two objectives: (1) maximizing flow coverage, i.e., measuring as many flows as possible, and (2) minimizing the distance between the control plane and switches that execute network measurement to enable timely data collection.

Input. The input comprises: (1) the network $G = ( V , E )$ ; (2) programmable switches $P \subseteq V$ supporting sketches and INT; (3) control plane nodes $C \subseteq V ; ( 4 )$ a set $\mathcal { F }$ of flows, where each flow $f \in { \mathcal { F } }$ only indicates an OD pair $\left( o _ { f } , d _ { f } \right) \left[ 1 0 , 2 5 \right]$ , where $o _ { f }$ and $d _ { f }$ are the ingress and egress of $f ,$ respectively; (5) for each flow $f ,$ the set $\mathcal { P } _ { f } \subseteq P$ of switches on any shortest path between $o _ { f }$ and $d _ { f } ;$ and (6) the distance metric $\delta : V \times C \to \mathbb { R } ^ { + }$ (e.g., hop count between meaurement points and control plane). Output. The output comprises: $( 1 ) x _ { p } \in \{ 0 , 1 \} \forall p \in P \colon x _ { p } = 1$ if sketch deployed at switch $p ; ( 2 ) \ : y _ { p } \in \{ 0 , 1 \} \forall p \in P \colon y _ { p } = 1$ if INT deployed at switch $p ; ( 3 ) \ u _ { p } \in \{ 0 , 1 \} \ \forall p \in P \colon u _ { p } = 1$ if switch $p$ is selected $( x _ { p } = 1 \lor y _ { p } = 1 ) ; ( 4 ) \ z _ { p , c } \in \{ 0 , 1 \}$ $\forall p \in P , c \in C \colon z _ { p , c } = 1$ if data from p sent to control node c; (5 $) w _ { f } \in \{ 0 , 1 \} \forall f \in \mathcal { F } : w _ { f } = 1$ if f is covered (measured). Objective. The objective refers to:

$$
\min -\alpha \sum_{f\in \mathcal{F}}w_{f} + (1 - \alpha)\sum_{\substack{p\in P\\ c\in C}}z_{p,c}\cdot \delta (p,c)\tag{1}
$$

in which the user-defined parameter $\alpha \in [ 0 , 1 ]$ balances the objective of maximizing coverage and that of minimizing the distances between selected switches and control plane nodes. MonPlan can also consider other objectives, e.g., minimizing the number of selected switches, which is elided for simplicity since this paper focuses on coverage.

TABLE I: Notation of major symbols used by this paper.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Symbol Description
G Network topology with switches V and links E
 $P \subseteq V$  Programmable switches supporting sketches and INT
 $C \subseteq V$  Control plane nodes
F Set of flows
 $o_{f}, d_{f}$  Orientation/destination of flow  $f \in F$ $P_{f}$  Programmable switches on any shortest path for flow f
 $F_{p}$  Flows that can be measured at switch p ( $\{f \mid p \in P_{f}\}$ )
 $\delta(p, c)$  Distance between switch p and control plane node c
 $\alpha$  Coverage-distance tradeoff parameter ( $0 \leq \alpha \leq 1$ )
 $\lambda_{f}$  Lagrange multiplier for flow f's coverage constraints
 $L(\lambda)$  Lagrangian dual function
 $\beta_{p}$  Switch penalty =  $\sum_{f \in F_{p}} \lambda_{f}$ $\gamma_{p}$  Data collection distance cost = (1 -  $\alpha$ )  $\min_{c \in C} \delta(p, c)$ $g_{f}$  Subgradient =  $\sum_{p \in P_{f}} u_{p} - w_{f}$ 
T Iteration count in subgradient optimization
 $\pi_{\theta}$  Trained RL policy network
 $P_{p,c}$  Selected network path from switch p to control plane node c
 $\pi_{p,c}$  Fraction of measurement data traffic from p to c
 $q_{e}^{t}$  Queue depth (bytes) on link e at time t
 $\Gamma_{p}^{total}$  Worst-case measurement data rate (bps) at switch p
 $\Gamma_{e}^{data}$  Normal data plane traffic rate (bps) on link e
 $\tau_{e}$  Safety threshold for congestion avoidance on link e
 $s_{t}$  State vector at time t for RL policy
 $x_{p}$  0-1 variable = 1 if sketch deployed at switch p
 $y_{p}$  0-1 variable = 1 if INT deployed at switch p
 $u_{p}$  0-1 variable = 1 if switch p is selected ( $x_{p} = 1 \lor y_{p} = 1$ )
 $z_{p,c}$  0-1 variable = 1 if data emitted from p to control plane node c
 $w_{f}$  0-1 variable = 1 if flow f is covered (i.e., measured)
</div>

Constraints. The problem has the following major constraints: Eqs. (2)-(4) bound the number of selected switches; Eq. (5) shows that when a flow $f$ is covered, at least one switch on the shortest paths that connect the OD pair of $f$ should be selected; Eq. (6) shows that each selected switch should send data to a control plane node; and Eq. (7) limits decision variables.

Selected switch number: $u _ { p } \geq x _ { p } \quad \forall p \in P$

$$
u _ {p} \geq y _ {p} \quad \forall p \in P\tag{2}
$$

$$
u _ {p} \leq x _ {p} + y _ {p} \quad \forall p \in P\tag{3}
$$

(4)

$$
\text { Coverage: } w _ {f} \leq \sum_ {p \in \mathcal {P} _ {f}} u _ {p} \quad \forall f \in \mathcal {F}\tag{5}
$$

$$
\text { Data   collection: } \sum_ {c \in C} z _ {p, c} = u _ {p} \quad \forall p \in P\tag{6}
$$

$$
0 - 1 \text {   decisions:   } x _ {p}, y _ {p}, u _ {p}, w _ {f}, z _ {p, c} \in \{0, 1 \}\tag{7}
$$

Hardness. This measurement point selection problem is NPhard. First, according to its dual combinatorial structures, this problem reduces to the set cover problem: each programmable switch $p \in P$ corresponds to the set $S _ { p } = \{ f \in \mathcal { F } \mid p \in \mathcal { P } _ { f } \}$ covering the flows possibly traversing $p .$ This step establishes a set system with the universe $U = { \mathcal { F } }$ and collection $S = \{ S _ { p } \}$ where maximizing coverage $\sum w _ { f }$ equals minimizing uncovered flows (i.e., a standard NP-hard set cover problem). Second, the objective of minimizing distances, i.e., $\sum z _ { p , c } \delta ( p , c )$ , forms an uncapacitated facility location subproblem, in which selected switches, i.e., $u _ { p } = 1$ , are facilities, control plane nodes in $C$ are clients, and $\delta ( p , c )$ are assignment costs.

To sum up, the joint objective Eq. (1) forms a multi-objective set cover with facility location costs. In particular, α modulates between flow coverage and resource efficiency: when $\alpha = 1$ the problem is an NP-hard set cover problem; when $\alpha = 0 ,$ , the problem is an NP-hard facility location problem.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Solve $L(\lambda)$

Require: $\lambda, G, \mathcal{F}, P, C, \delta, \alpha$ (See Table I)
Ensure: $L(\lambda)$, primal variables
1: Initialize $u_p = 0$, $w_f = 0$ $\forall p \in P, f \in \mathcal{F}$
2: for each switch $p \in P$ do
3: Compute $\beta_p = \sum_{f:p \in \mathcal{P}_f} \lambda_f \quad \triangleright$ Aggregate flow penalties
4: Compute $\gamma_p = (1 - \alpha) \min_{c \in C} \delta(p, c) \triangleright$ Minimize distance costs
5: if $\beta_p &gt; \gamma_p$ then $\triangleright$ Penalties overwhelm benefits
6: Set $u_p = 1$
7: Assign $z_{p,c^*} = 1$ for $c^* = \arg\min_c \delta(p, c)$
8: for each flow $f \in \mathcal{F}$ do
9: if $\exists p \in \mathcal{P}_f : u_p = 1$ then
10: Set $w_f = 1$
11: return $L(\lambda) = \sum_p u_p(\beta_p + \gamma_p) + \sum_f w_f(-\alpha - \lambda_f)$
</div>

Solving. Given the NP hardness, directly solving the problem using commercial MIP solvers such as Gurobi [37] and CPLEX [38] inevitably suffers from excessively long execution time or fails to find possible solutions. In response, MonPlan employs Lagrangian relaxation as follows.

We relax the coverage constraints using Lagrange multipliers $\lambda _ { f } \geq 0$ . The Lagrangian is:

$$
\begin{array}{l} L (\boldsymbol {\lambda}) = \min _ {\mathbf {u}, \mathbf {w}, \mathbf {z}} \left[ - \alpha \sum_ {f \in \mathcal {F}} w _ {f} + (1 - \alpha) \sum_ {p \in P, c \in C} z _ {p, c} \delta (p, c) \right. \\ \left. + \sum_ {f \in \mathcal {F}} \lambda_ {f} \left(\sum_ {p \in \mathcal {P} _ {f}} u _ {p} - w _ {f}\right) \right] = \min _ {\mathbf {u}, \mathbf {w}, \mathbf {z}} \left[ \underbrace {\sum_ {p \in P} u _ {p} \left(\sum_ {f : p \in \mathcal {P} _ {f}} \lambda_ {f}\right)} _ {\text {Switch penalty}} \right. \\ \left. + \underbrace {\sum_ {f \in \mathcal {F}} w _ {f} (- \alpha - \lambda_ {f})} _ {\text {Coverage reward}} + \underbrace {(1 - \alpha) \sum_ {p \in P , c \in C} z _ {p , c} \delta (p , c)} _ {\text {Data collection distance cost}} \right] \end{array} \tag {8}
$$

where $\lambda _ { f }$ is the Lagrange multiplier for flow $f$ and quantifies the penalty weight for not covering $f .$ The switch penalty refers to the penalty for selecting a switch. It represents that selecting a switch needs to pay the penalty of covering all its measurable flows. Therefore, it transforms the original coverage constraints into switch selection penalties that balance against the reward of covering flows and the distance cost of transferring data from selected switches to the control plane.

In this context, the dual of the Lagrangian relaxation is:

$$
\max _ {\lambda_ {f} \geq 0} L (\boldsymbol {\lambda}), \text {   s.t.   Eqs.   (2) - (7)   }\tag{9}
$$

According to the above relaxation, MonPlan uses a masterslave algorithm to solve the problem: Algorithm 2 is the master that controls the optimization while Algorithm 1 is the slave that is invoked in each iteration to solve the Lagrangian subproblem. Specifically, Algorithm 2 iteratively tunes Lagrange multipliers λ to maximize the dual function. In each iteration $t ,$ it (i) inputs $\boldsymbol { \lambda } ^ { ( t ) }$ to Algorithm 1, (ii) receives primal variables $u _ { p } , w _ { f } , z _ { p , c }$ and the dual bound $L ( \lambda )$ , (iii) computes the normalized subgradient $g _ { f } ^ { ( t ) }$ , and (iv) updates $\lambda ^ { ( t + 1 ) }$ and records the best solution.

In the step (i) of each iteration in Algorithm 2, Algorithm 1 computes the optimal deployments for given λ: for each switch $p ,$ it calculates the flow penalty $\beta _ { p }$ and collection cost $\gamma _ { p } .$ . If $\beta _ { p } > \gamma _ { p } ,$ , it selects p to activate measurement, i.e., $u _ { p } = 1 \ d s$ and assigns $p$ to the nearest control plane node, i.e., $z _ { p , c ^ { * } } = 1$ Next, for each flow $f ,$ it marks $w _ { f } = 1$ if there exists at least one selected switch on the flow’s path $( \mathrm { i . e . , } \exists p \in \mathscr { P } _ { f } : u _ { p } = 1 )$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Subgradient Optimization for Dual Problem
Require: Max iterations T,  $\epsilon = 10^{-6}$ 
Ensure:  $\max_{t} L(\boldsymbol{\lambda}^{(t)})$ 

1: Initialize  $\lambda_{f}^{(0)} = 0.5, \forall f \in \mathcal{F}, t = 0$ 

2:  $L_{best} \leftarrow -\infty, \lambda_{best} \leftarrow \boldsymbol{\lambda}^{(0)}$ 

3: while t &lt; T do

4: Solve  $L(\boldsymbol{\lambda}^{(t)})$  using Algorithm 1

5: Compute subgradient  $g_{f}^{(t)} = \sum_{p \in \mathcal{P}_{f}} u_{p}^{*} - w_{f}^{*} \forall f \in \mathcal{F}$ 

6: Compute gradient norm  $\|g^{(t)}\| = \sqrt{\sum_{f}(g_{f}^{(t)})^{2}}$ 

7: Compute step size  $\theta_{t} = \frac{1}{\sqrt{t+1}} \cdot \frac{|L(\boldsymbol{\lambda}^{(t)})|}{\max(\|g^{(t)}\|^{2}, \epsilon)}$ 

8: for each flow  $f \in F$  do

9:  $\lambda_{f}^{(t+1)} = \max\left(0, \min\left(2, \lambda_{f}^{(t)} + \theta_{t} g_{f}^{(t)}\right)\right)$ 

10: if  $L(\boldsymbol{\lambda}^{(t)}) &gt; L_{best}$  then

11:  $L_{best} \leftarrow L(\boldsymbol{\lambda}^{(t)})$ 

12:  $\lambda_{best} \leftarrow \boldsymbol{\lambda}^{(t)}$ 

13:  $t \leftarrow t + 1$ 

14: return  $L_{best}, \lambda_{best}$
</div>

Theorem 1 (Weak Duality). The optimal dual value $d ^ { * } =$ max<sub>λ</sub> L(λ) is a lower bound on the primal optimal value $p ^ { * }$ Proof. For any feasible primal solution $( \mathbf { u } , \mathbf { w } , \mathbf { z } )$ and $\lambda \geq 0 \colon$

$$
\begin{array}{l} L (\boldsymbol {\lambda}) \leq - \alpha \sum_ {f \in \mathcal {F}} w _ {f} + (1 - \alpha) \sum_ {p \in P, c \in C} z _ {p, c} \delta (p, c) \\ \quad + \sum_ {f \in \mathcal {F}} \lambda_ {f} \left(\sum_ {p \in \mathcal {P} _ {f}} u _ {p} - w _ {f}\right) \\ \quad \leq - \alpha \sum_ {f \in \mathcal {F}} w _ {f} + (1 - \alpha) \sum_ {p \in P, c \in C} z _ {p, c} \delta (p, c) \\ = p _ {\mathrm{obj}} \quad (\text {since} \sum_ {p \in \mathcal {P} _ {f}} u _ {p} - w _ {f} \geq 0 \text {by Eq. (5))} \end{array}
$$

where $p _ { \mathrm { o b j } }$ is the primal objective value for a feasible solution in the measurement point selection problem. Thus, $d ^ { * } \leq p ^ { * }$ □

Theorem 2 (Optimality Gap). Let $( \mathbf { u } ^ { * } , \mathbf { w } ^ { * } , \mathbf { z } ^ { * } )$ be the primal optimal solution. The optimality gap satisfies:

$$
p ^ {*} - d ^ {*} \leq \sum_ {f \in \mathcal {F}} \lambda_ {f} ^ {*} \left(\sum_ {p \in \mathcal {P} _ {f}} u _ {p} ^ {*} - w _ {f} ^ {*}\right)
$$

where $\lambda ^ { * }$ are the optimal dual multipliers.

Proof. From complementary slackness:

$$
\begin{array}{l} p ^ {*} - d ^ {*} = \left[ - \alpha \sum_ {f \in \mathcal {F}} w _ {f} ^ {*} + (1 - \alpha) \sum_ {p \in P, c \in C} z _ {p, c} ^ {*} \delta (p, c) \right] - L (\boldsymbol {\lambda} ^ {*}) \\ = \sum_ {f \in \mathcal {F}} \lambda_ {f} ^ {*} \left(w _ {f} ^ {*} - \sum_ {p \in \mathcal {P} _ {f}} u _ {p} ^ {*}\right) \\ \leq 0 \quad (\text { because } w _ {f} ^ {*} \leq \sum_ {p \in \mathcal {P} _ {f}} u _ {p} ^ {*} \text { and } \lambda_ {f} ^ {*} \geq 0) \end{array}
$$

The gap equals the sum of violated coverage constraints scaled by $\lambda _ { f } ^ { \ast }$ □

## V. LOSS-FREE MEASUREMENT DATA COLLECTION

Overview. After making decisions on which switches to measure traffic, MonPlan determines which network paths to safely transfer measurement data from switches to control plane nodes without incurring congestion. It executes a two-step workflow. First, it estimates the worst-case sending rate (i.e., maximum) of sketch data and INT data in each switch. Second, according to its estimates, it picks paths to transfer data without congestion. Estimating worst-case sending rates. MonPlan models both sketch and INT data. For sketch data, the worst-case sending rate $\gamma _ { k } ^ { \mathrm { s k e t c h } }$ for sketch k is determined by:

$$
\gamma_ {k} ^ {\mathrm{sketch}} = \frac {S _ {k}}{T _ {k}}\tag{10}
$$

where $S _ { k }$ and $T _ { k }$ refer to the sketch size in bytes and the collection window in seconds, respectively. This equation denotes that the data recorded in sketch counter arrays are periodically flushed to the control plane at the end of each window, $\mathrm { e . g . }$ for the sketch with 10 MB memory, a measurement window of 1 ms corresponds to $\begin{array} { r } { \ i \gamma _ { k } ^ { \mathrm { s k e t c h } } = \frac { 1 0 ^ { 6 } \mathrm { b y t e s } } { 1 0 ^ { - 3 } \mathrm { s } } = 8 \mathrm { G b p s } } \end{array}$

For INT data, the worst-case rate $\gamma _ { p } ^ { \mathrm { I N T } }$ at switch $p$ is:

$$
\gamma_ {p} ^ {\mathrm{INT}} = \left(\frac {C _ {p} \times \phi}{\mu}\right) \times B _ {\mathrm{INT}}\tag{11}
$$

where $C _ { p }$ refers to the bandwidth capacity of each link while $\phi$ is the maximum possible fraction of link bandwidth that can be consumed by small flows. ϕ can be obtained by analyzing historical traffic data [21]. $C _ { p } \times \phi$ denotes the maximum possible byte rate contributed by small flows on a link. Moreover, since INT overheads are per-packet, MonPlan converts the byte rate of $C _ { p } \times \phi$ to the packet rate to estimate INT overheads, where $\mu$ denotes the average packet size in small flows. As such, the maximum packet rate of small flows is $\frac { C _ { p } \times \phi } { \mu }$ . Thus, Eq. (10) estimates the bandwidth overheads consumed by INT headers per second, where $B _ { \mathrm { I N T } }$ is the size of INT headers per packet.

To sum up, the maximum possible rate of sending measurement data at switch $p$ is estimated as

$$
\Gamma_ {p} ^ {\mathrm{total}} = \sum_ {k \in \mathcal {K} _ {p}} \gamma_ {k} ^ {\mathrm{sketch}} + \gamma_ {p} ^ {\mathrm{INT}}\tag{12}
$$

where ${ \boldsymbol { \kappa } } _ { p }$ is the set of sketches at $p .$

Reinforcement learning (RL) for dynamic path selection. Given the worst-case estimates in $\{ \Gamma _ { p } ^ { \mathrm { t o t a l } } \}$ }, MonPlan formulates dynamic path selection based on a constrained Markov decision process (CMDP) to avoid saturating network paths, i.e.

$$
\min _ {\pi} \mathbb {E} \left[ \sum_ {t = 0} ^ {T} \sum_ {e \in E} q _ {e} ^ {t} \right]\tag{13}
$$

$$
\text { s.t. } \quad \sum_ {c \in C} \pi_ {p, c} = 1 \quad \forall p \in P\tag{14}
$$

$$
\Gamma_ {e} ^ {\mathrm{meas}} \leq \tau_ {e} C _ {e} - \Gamma_ {e} ^ {\mathrm{data}} \quad \forall e \in E\tag{15}
$$

where $q _ { e } ^ { t }$ denotes the queue length in bytes on link e at time $t ;$ $\pi _ { p , c }$ is the fraction of measurement data streams from switch $p$ to control plane node $c ; \Gamma _ { e } ^ { \mathrm { m e a s } }$ quantifies the measurement data streams on link e, i.e.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 Congestion-free path selection
Require: Trained policy network $\pi_{\theta}$, network $G$, control plane nodes in $C$, programmable switches in $P$, worst-case rates $\{\Gamma_p^{\text{total}}\}_{p \in P}$, safety threshold $\tau$
Ensure: Selected paths in $\{\mathcal{P}_{p,c}\}$ and splitting ratios in $\{\pi_{p,c}\}$
1: Initialize $\{\mathcal{P}_{p,c}\} \leftarrow \text{K-SHORTESTPATHS}(G, P, C)$
2: Initialize $\pi_{p,c} \leftarrow \frac{1}{|C|}$ ▷ Uniform initial splitting
3: loop ▷ At each time step $t$
4: Collect $\Gamma_e^{\text{data}}$ and $q_e^t$
5: Build state $s_t \leftarrow \left( \{ \frac{\Gamma_e^{\text{data}}}{C_e} \}, \{ q_e^t \}, \{ \Gamma_p^{\text{total}} \} \right)$
6: Obtain action $a_t \leftarrow \pi_\theta(s_t)$ and yield ($\{\mathcal{P}_{p,c}\}, \{\pi_{p,c}\}$)
7: Compute $\Gamma_e^{\text{meas}} \leftarrow \sum_p \sum_c \pi_{p,c} \cdot \Gamma_p^{\text{total}} \cdot \mathbb{I}_{e \in \mathcal{P}_{p,c}}$
8: $\pi_{p,c} \leftarrow \pi_{p,c} \cdot \min \left( 1, \frac{\tau C_e - \Gamma_e^{\text{data}}}{\Gamma_e^{\text{meas}} + \epsilon} \right)$ for $e \in \mathcal{P}_{p,c}$
9: $\pi_{p,c} \leftarrow \frac{\pi_{p,c}}{\sum_c \pi_{p,c}} \quad \forall p \in P$ ▷ Normalization
10: Deploy $\mathcal{P}_{p,c}$ and $\pi_{p,c}$ on switches
</div>

$$
\Gamma_ {e} ^ {\mathrm{meas}} = \sum_ {p} \sum_ {c} \pi_ {p, c} \cdot \Gamma_ {p} ^ {\mathrm{total}} \cdot \mathbb {I} _ {e \in \mathcal {P} _ {p, c}}\tag{16}
$$

where $\mathbb { I } _ { e \in \mathcal { P } _ { p , c } } = 1$ if link e belongs to path $\mathcal { P } _ { p , c } ; \Gamma _ { e } ^ { \mathrm { d a t a } }$ quantifies data plane traffic on $e ;$ and $\tau _ { e }$ represents the safety threshold that avoids congestion (e.g., 0.8 of the link capacity).

Here, the inputs include $q _ { e } ^ { t } , C _ { e } , \Gamma _ { p } ^ { \mathrm { t o t a l } } , \mathbb { I } _ { e \in \mathcal { P } p , c } , \bar { \Gamma _ { e } ^ { \mathrm { d a t a } } }$ , and $\tau _ { e }$ MonPlan obtains them as follows: $q _ { e } ^ { t }$ is collected by INT; $C _ { e }$ is the link capacity that is already known in topology information; $\Gamma _ { p } ^ { \mathrm { t o t a l } }$ is computed by $\mathrm { E q . l 2 } ; \mathbb { I } _ { e \in \mathcal { P } p , c }$ is calculated via shortest path algorithms such as Dijkstra; $\Gamma _ { e } ^ { \mathrm { d a t a } }$ can be direcly obtained using existing techniques such as sFlow [39] and NetFlow [40]; and $\tau _ { e }$ is user-configurable.

Next, the output of MonPlan includes (i) which paths, i.e., ${ \mathcal { P } } _ { p , c } ,$ to transfer measurement data from switch $p$ to control plane node $c ,$ and (ii) split ratios, $\mathrm { i . e . , } \ \pi _ { p , c } ,$ , that decide how to allocate measurement traffic across these paths.

Then MonPlan solves the CMDP as follows. First, it trains the policy $\pi _ { \theta }$ via offline constrained policy optimization (CPO) [41]. Such training employs a simulated network environment with the following components:

$$
\bullet \text {   State:   } s _ {t} = \big (\{\Gamma_ {e} ^ {\text { data }} / C _ {e} \}, \{q _ {e} ^ {t} \}, \{\Gamma_ {p} ^ {\text { total }} \} \big).
$$

• Action: (1) paths in $\{ \mathcal { P } _ { p , c } \} _ { { } }$ , and (2) splitting ratios $\pi _ { p , c } .$ • Reward: $\begin{array} { r } { r _ { t } = - \sum _ { e \in E } q _ { e } ^ { t } - \eta \cdot \mathbb { I } _ { \mathrm { v i o l a t i o n } } , } \end{array}$ , where $- \textstyle \sum _ { e \in E } q _ { e } ^ { t }$ encourages RL to minimize network congestion, and η · I<sub>violation</sub> penalizes constraint violations: η is a large penalty weight $( \mathrm { e . g . , 1 0 ^ { 6 } } )$ and $\mathbb { I } _ { \mathrm { v i o l a t i o n } } = 1 \mathrm { i f } \Gamma _ { e } ^ { \mathrm { d a t a } } + \Gamma _ { e } ^ { \mathrm { m e a s } } > \tau C _ { e }$ for any $e _ { \cdot }$ With the above components, MonPlan maximizes $r _ { t }$ while satisfying Eq. (15) through Lagrangian relaxation. After around $1 0 ^ { 5 }$ training steps with real traffic traces $( { \mathrm { e . g . , C A I D A } } ) , \pi _ { \theta }$ is converged and is deployed for online inference.

With $\pi _ { \theta } ,$ MonPlan proposes an RL framework (Algorithm 3). Initially (lines 1-2), it precomputes k candidate paths in $\{ \mathcal { P } _ { p , c } \}$ between all $p – c$ pairs and initializes uniform splitting ratios, i.e., $\pi _ { p , c } = 1 / | C |$ . At each timestep t (loop in line 3), $q _ { e } ^ { t }$ and $\Gamma _ { e } ^ { \mathrm { d a t a } }$ are collected and transformed into state $s _ { t }$ (lines 4-5). Then, the RL policy $\pi _ { \theta }$ yields path selections and raw splitting ratios (line 6). After computing $\Gamma _ { e } ^ { \mathrm { m e a s } }$ via $\mathrm { E q . l 6 }$ (line 7), MonPlan enforces bandwidth constraints via scaling and normalization (lines 8-9).

![](images/acf6e9b45347908a654f0f8c140396d944ce7a6f971382e66fa0c51a8530bbf6.jpg)  
Fig. 2: Example of path selection in MonPlan.

Finally, selected paths $\mathcal { P } _ { p , c }$ and splitting ratios $\pi _ { p , c }$ are deployed onto data plane switches, e.g., via rule installation (line 10). In short, the algorithm dynamically optimizes path utilization to prevent congestion during measurement data collection.

Example. Figure 2 is the triangle of three switches, $p _ { 1 } , p _ { 2 } , p _ { 3 }$ All links are 10-Gbps. The control plane is directly connected to $p _ { 2 }$ . Five flows traverse the network: a video flow $f _ { 1 }$ with the OD pair of $( p _ { 1 } , p _ { 2 } )$ , a RPC flow $f _ { 2 }$ with the OD pair of $( p _ { 1 } , p _ { 3 } )$ a database flow $f _ { 3 }$ with the OD pair of $( p _ { 2 } , p _ { 3 } )$ , an IoT flow $f _ { 4 }$ with the OD pair of $( p _ { 3 } , p _ { 1 } )$ , and a backup flow $f _ { 5 }$ with the OD pair of $( p _ { 3 } , p _ { 2 } ) . f _ { 1 } , f _ { 3 } ,$ , and $f _ { 5 }$ are large flows while small flows are $f _ { 2 }$ and $f _ { 4 } .$ . The safety threshold $\tau$ is 0.8 of link capacity. Suppose that MonPlan selects $p _ { 2 }$ to run sketches and cover all large flows. For small flows, $p _ { 1 }$ monitors $f _ { 2 } ; p _ { 3 }$ monitors $f _ { 4 }$

Consider the state $s _ { t } \colon ( 1 )$ link utilizations: $p _ { 1 }  p _ { 3 } = 2 0 \%$ $p _ { 2 }  p _ { 3 } = 7 0 \% , p _ { 1 }  p _ { 2 } = 2 0 \% ; ( 2 )$ queue depths: 40 KB in each switch; (3) worst-case measurement data rates: $\Gamma _ { p _ { 1 } } ^ { \mathrm { t o t a l } } =$ 3 Gbps, $\Gamma _ { p _ { 2 } } ^ { \mathrm { t o t a l } } = 1$ Gbps, and $\Gamma _ { p _ { 3 } } ^ { \mathrm { t o t a l } } = 2$ Gbps. The RL policy π<sub>θ</sub> in MonPlan decides to (1) deliver 100% $p _ { 1 } \mathrm { ^ { \circ } s }$ INT data using the path $p _ { 1 }  p _ { 2 }$ , and (2) deliver 100% $\vec { p _ { 3 } } \ '$ INT data using the path $p _ { 3 }  p _ { 1 }  p _ { 2 }$ . This avoids congesting other paths, e.g., for the path $p _ { 1 }  p _ { 2 } , \Gamma _ { p _ { 1 } } ^ { \mathrm { t o t a l } } + \Gamma _ { p _ { 3 } } ^ { \mathrm { t o t a l } } + 2 0 \% \times 1 0 \mathrm { G } \mathsf { b } \mathsf { p } \mathrm { s } = 7 \mathrm { G } \mathsf { b } \mathsf { p } \mathrm { s } < \tau \times$ $1 0 \mathrm { G b p s } { = } 8 \mathrm { G b p \bar { s } }$ , preserving the safety threshold. Otherwise, $\mathrm { i f } \ p _ { 3 }$ sends INT data to $p _ { 2 }$ , the link $p _ { 2 }  p _ { 3 }$ suffers from the load of 8 Gbps, which violates the safety threshold $\tau { : } \Gamma _ { p _ { 3 } } ^ { \mathrm { t o t a l } } +$ $7 0 \% \times 1 0 \mathrm { G b p s } = 9 \mathrm { G b p s } > \tau \times 1 0 \mathrm { G b p s } = 8 \mathrm { G b p s }$

## VI. EVALUATION

Implementation. Our implementation comprises optimization algorithms and a controller. For the optimization algorithms, we implement the Lagrangian relaxation algorithms for measurement point selection (§IV) in C++ using the Gurobi API [37]. The RL algorithm for congestion-free data collection (§V) is implemented using PyTorch with the CPO library [42]. Next, we implement a controller in Python that translates optimization outputs $( \mathrm { i } . \mathrm { e } . , x _ { p } , y _ { p } , z _ { p , c }$ variables) into switch configurations. Specifically, it configures: (1) sketch deployment and INT activation on selected switches via data plane program deployment [43, 44], and (2) data routing rules inside match-action tables to direct measurement data to target paths. The controller uses the Tofino SDE [24] to load configurations on switches.

Testbed and simulator. We construct a real testbed comprising six 32 × 400 Gbps Tofino2 programmable switches [24]. These switches are interconnected within a two-level fat-tree topology via 100-Gbps links. Also, at the network edge, we establish a cluster of high-performance servers, each offering 36-core Intel Xeon Gold 6240C 2.60 GHz CPU and 128-GB RAM, as the control plane. For traffic generation, we connect eight servers that runs PktGen-DPDK [45] at line rate to the network. Next, due to limited testbed scale, we implement a simulator in NS3 to simulate large-scale topologies that models: (1) switch pipelines with resource constraints [46], (2) link bandwidths and latency, and (3) switch and control-plane performance statistics based on real-world measurements. The simulator accepts real traffic traces such as CAIDA [22] and topology files as input.

Topologies and workloads. We simulate two typical classes of topologies [25, 47]. (1) Wide-area networks (WANs). We select five WANs, AboveNet (20 switches), Internet2 (42 switches), ForthNet (62 switches), Bestel (83 switches), and Interroute (109 switches), from the Internet topology zoo [48]. We denote these topologies with T1-T5. We set the transmission latency of each link to be randomly distributed in [10 ms, 50 ms] [47] while setting all switches to be programmable. (2) Data center networks (DCNs). For DCNs, we consider the fat-tree networks and vary the pod number: C1-C5 that use 16, 20, 24, 32, and 48 pods, respectively, e.g., C5 has 2880 switches and 55296 links. We set the link latency to be randomly varied between $1 \mu \mathrm s$ to $1 0 \mu \mathrm { s }$ . We randomly select 30% of switches to be programmable based on recent statistics [49]. For each programmable switch, we set its configurations based on real switches [46].

For control plane nodes, we leverage two distinct strategies for WANs and DCNs, respectively. For WANs, we employ the technique that optimizes the placement of control plane nodes in WANs [50]. For DCNs, we allocate a distinct control plane node to each pod of fat-tree networks.

We choose corresponding workloads that match WANs and DCNs. For WANs, we choose a CAIDA trace [22] that lasts for one minute and comprises around 26 M packets. For DCNs, we use the complete IMC DCN traffic trace [23]. Each flow’s OD pair is randomly selected among edge switches.

Baselines. We compare MonPlan with five types of techniques. 1 Sketches only. We implement five state-of-the-art sketches, including the count-min sketch (CM) [51], the count sketch (CS) [29], the elastic sketch (ES) [8], FlowRadar (FR) [7], and UnivMon (UM) [10]. We refer to their original papers to configure their parameters to maximize accuracy.

2 INT only. We consider three classic INT techniques, including INT [33], PINT [5], and DeltaINT (i.e., ∆INT) [6]. We implement them based on their open-source implementations.

3 Hybrid sketch+INT. We implement open-source SketchINT (SI) [18] and LightGuardian (LG) [19].

4 Measurement point selection algorithms. We choose three algorithms for selecting measurement points, i.e., MTP [4] that aims to minimize the number of occupied measurement points to place sketches and INT, SPEED [43] that optimizes both resources and performance, and a Greedy-based heuristic that prioritizes the switches with more resources.

![](images/4ff7142de2263cae404579174492cd54224fef2b53e192b58e2181455a9d5c96.jpg)  
(a) HH (CAIDA).

![](images/bdb6a75a28e259fd7771a081bae71853096c006ff5a260d9f96f2da92e6a58b7.jpg)  
(b) HH (IMC).

![](images/b315f964e8371ecb767af459ef9c671c5d1073f8f8121f028fccb3db1a5e3710.jpg)  
(c) SS (CAIDA).

![](images/68683b3bcfbccdf89f9550f34298046aba0b04a93a1f0babacf6a2c45ee77761.jpg)  
(d) SS (IMC).

![](images/c0ca17d949cea53144577e69feb6101be9233d9ee7776b1fafc3e8d2dfd28616.jpg)  
(e) DF (CAIDA).

![](images/00a96dd7fd1b326ca03db641910563a9ba7795620d9a1732d997f5a1b9204855.jpg)  
(f) DF (IMC).

![](images/cad472a0903a13343c8261d1ba22e3306e34d266bff600d83bd999ba6d2740ba.jpg)  
(g) GI (CAIDA).

![](images/a190d1ffd3f0c4b60735a96717ff69209056da10d0afefc496d162196123ebd0.jpg)  
(h) GI (IMC).

![](images/0662dbc987eae51ab96bede2df6f95f23e7334867eb0004372d18890bb9b6a2e.jpg)  
(i) PC (CAIDA).

![](images/0af13e9e5522dca9bcdda229fef2deb8c85014716a39ab0c569c786813d0fb20.jpg)  
(j) PC (IMC).

Fig. 3: Accuracy for volumetric applications.  
![](images/930066b545cdb00dc41432f5d5345f28e6519e84dddb5d73c4b25c4f61ad517e.jpg)  
(a) Sending rate.

![](images/9407fc632882fb43ed9adee330f25ca05e3e0a47e2ca52509f5c9d76d465c0ae.jpg)  
(b) Data loss.  
Fig. 4: Overheads for volumetric applications.

5 Data collection path selection algorithms. We use three algorithms for selecting the paths of transferring measurement data, i.e., Escala [52] that selects the paths with lower latency, a randomized algorithm that randomly chooses its paths, and INT-Path [16] that adopts a depth-first search (DFS) heuristic to cover as many measurement points as possible.

For a fair comparison, we set the top three types of techniques to select the same measurement points and paths chosen by the algorithms of MonPlan. We fix the amount of switch memory allocated to each sketch or INT to 10 MB, which is close to the maximum capacity of a switch [30]. Moreover, to quantify the solution quality of point/path selection algorithms, we also use Gurobi [37] to find the optimal decisions (i.e., OPT).

![](images/8f5ea5e0933a673a0e8ef24dca28e5c7b12baed54e9306416ed2176de41731fb.jpg)  
(a) EE.

![](images/dc4f4b24a2588ddb70d16cbbd9eba6e5df710f31be0523d284ca230ab114366c.jpg)  
(b) FD.

Fig. 5: Accuracy for aggregated applications.  
![](images/66db5a543f03606a49e27737f52f164683dc1b1e9b3af237f56164d67da4c111.jpg)  
(a) CC (Web).

![](images/f4cd9807fbe103fcf21a1248ad52edc84ae965ee708b1942c2d1e63bce07c7a8.jpg)  
(b) CC (Hadoop).

![](images/deb3bb4a62d0f22a6ab5a994ec96b681d5efe86e77a3db74a2b567c75368a90a.jpg)  
(c) MD (Recall).

![](images/35e101cb6550fb8c4e9c2667f4f71676e148c01ae5924f1464d9965d2873dc38.jpg)  
(d) MD (F1 score).  
Fig. 6: Benefits for troubleshooting applications.

Applications. We consider three types of applications:

• Volumetric applications include the detection of heavy hitter (HH) [3], superspreaders (SS) [53], DDoS flows (DF) [32], global icebergs (GI) [10], and per-flow counting (PC) [3].

• Aggregated applications include entropy estimation (EE) [10] and flow size distribution (FD) [4] that summarize all flows.

• Troubleshooting applications of microburst detection (MD) and congestion control (CC) [5, 6] query per-flow metadata.

MonPlan brings accuracy and efficiency benefits to diverse applications. In our testbed, we use MonPlan and baselines to measure traffic, respectively. We replay CAIDA traces [22] to our testbed and set the OD pair of each flow to random edge switches. The control plane runs the applications to identify the flows of their interest based on collected data. We compute the accuracy by comparing measured data with the ground truth obtained by analyzing input traces.

## (1) Evaluation with volumetric applications

We set the thresholds of HH and GI to 10K packets [10], set the threshold of SS to 0.5% of the total number of IP addresses [53], and set the threshold of DF to 0.5% of the total number of five-tuples [4]. PC considers per-flow packet counts. We use F1 scores, 2tp/(2tp+fp+fn), where tp, fp, and fn are the number of true positives, false positives, and false negatives.

For HH, SS, DF, GI (Figure 3), MonPlan improves accuracy by 23∼95%. This benefit originates from co-designing sketches and INT: sketches enable accurate measurement for large flows while INT mitigate the errors of measuring small flows, while using only sketches or INT alone drops accuracy: small flows in sketches suffer from hash collisions with large flows, while direct INT brings congestion and data loss.

For PC, in Figure 3, MonPlan achieves near-optimal accuracy because it employs fully accurate INT for small flow.

![](images/270612794529e248c727d1404220e9ed8b8f4a11978610c36e33155b95360c6f.jpg)  
(a) Coverage (WAN).

![](images/7edca101602e154a4540fc3698757e63691f3d66d54ede1ba0863a01bcd217f7.jpg)  
(b) Coverage (DCN).

![](images/3f78181f68ac308acd1ff4e5de7b3cdce32274091565b521dcec524285c71061.jpg)  
(c) Time (WAN).

![](images/d7d6c412ee948a9c85767b2653e19f1e5d87b5f668a64ce56743237e4b4160ed.jpg)  
(d) Time (DCN).  
Fig. 7: Near-optimal and timely measurement point selection.

Figure 4 presents the overheads of MonPlan when transfering data to the control plane. Compared with INT, MonPlan reduces the rate of transferring data by an order of magnitude when we manually increase traffic rate from 20% to 80% of switch capability. Such a benefit comes from our design that only small flows trigger INT, thus limiting overheads and avoids data loss.

## (2) Evaluation with aggregated applications

For EE, we only consider FR and UM since only those two sketch-only baselines support EE. Figure 5 shows that MonPlan reduces its estimation errors and produces an entropy near the true one. Again, this improvement comes from the accuracy of measuring small flows via INT in MonPlan.

For FD, we set the flow identifier to two-tuple. In Figure 5, MonPlan offers near-optimal distributions (i.e., close to the ground truth, “Ideal”) as it preserves the high accuracy of perflow packet counts. In contrast, other baselines suffer from nontrivial accuracy loss due to the miss of small flows or data loss incurred by congestions during measurement data transmission.

## (3) Evaluation with troubleshooting applications

For CC, we exploit HPCC [54] for congestion control that adjusts the servers’ sending rates with respect to collected link utilization. We replay Web search [55] and Hadoop workloads [21] in our testbed. The metric we use to evaluate congestion control is slowdown, which equals the ratio between the completion time of a flow when all other flows exist and when only the flow itself exists. A smaller slowdown corresponds to better congestion control. We consider the 95th percentile slowdown for each flow size. In Figure 6, MonPlan achieves more accurate congestion control, enabling lower flow completion time.

For MD, microbursts have been considered as the common root cause for sporadic excessive delays and packet loss. Thus, MD detects microbursts by monitoring switch queuing delays. If a queuing delay exceeds the pre-defined threshold, INT-based techniques will report data to the control plane for microburst analysis [56]. We replay the above Hadoop workload [21] while generating microbursts by injecting short-lived 10-100 µs UDP flows and increasing the number of synthetic microbursts from 5 to 20. In Figure 6, MonPlan improves baselines with higher accuracy of detecting microbursts. Such benefits come from its accuracy of measuring all flows with resource efficiency.

MonPlan achieves near-optimal measurement point selection. We invoke MonPlan and the comparison solutions to select measurement points in WANs and DCNs, respectively. Figure 7 presents the flow coverage of decisions made by each technique. It indicates that MonPlan covers most flows even with unknown routing information, while other techniques fail to provide high coverage. Our algorithms also optimize the distances between switches and control plane nodes, yielding near-optimal results.

![](images/1f9cde05778bd937f31b287707c69b9258ceef69055a95ff6d94e24747a14ede.jpg)  
(a) # of congested links (WAN).

![](images/2fb23d8cfd969725901da99d89025ade6a19e44a490183011cf65c17b85d7919.jpg)  
(b) # of congested links (DCN).

![](images/d641fda8fde15116f708b5ca69243ab9e29cc2b82e0b81672cf0ab0763f50dda.jpg)  
(c) Loss rate (WAN).

![](images/7ce7bc811c0fe1500a771f63eafd185df5f87dfde6e2945103ced91cbd75b2ef.jpg)  
(d) Loss rate (DCN).  
Fig. 8: Loss-free measurement data collection.

We also measure the execution time of MonPlan. Figure 7 indicates that through Lagrangian relaxation, MonPlan reduces the time by an order of magnitude when compared with OPT. MonPlan achieves near-optimal data collection path selection. We invoke MonPlan and the comparison solutions to select network paths for transferring measurement data, respectively. Figure 8 computes the number of congested links incurred by the decisions made by each technique. MonPlan prevents link congestions in its collection, while other techniques bring nontrivial congestions, leading to high data loss rates of 10∼42%. Also, its RL algorithm maintains timeliness, which selects paths within a few milliseconds. Hence, it is acceptable for handling runtime dynamics with loss-free measurement data collection.

## VII. CONCLUSION

We propose MonPlan, a framework that co-designs sketches and INT to measure large and small flows respectively for accurate and resource-efficient network measurement. To enable such a co-design, MonPlan solves the NP-hard measurement point selection with the near-optimal Lagrangian relaxation. It offers congestion-free data collection with worst-case rate estimations of sending measurement data and RL-based dynamic path selection. We implement MonPlan on 32×400 Gbps Tofino switches. Our testbed experiments indicate that MonPlan offers 23∼95% accuracy improvement and resource efficiency.

Acknowledgement. We sincerely thank anonymous reviewers. This work is supported by National Key Research and Development (R&D) Program of China (2023YFB2904000), National Natural Science Foundation of China (No. 623B2090), Joint Funds of the National Natural Science Foundation of China (No. U25B2024, and No. U25B2038), Research Grants Council of Hong Kong (GRF 14201523), Natural Science Foundation of Fujian Province of China (No. 2024J08277), and Science Foundation of the Fuzhou (No. 2025-ZD-023).

## REFERENCE

[1] H. Huang, C. Lou, Y.-E. Sun, Y. Du, S. Chen, G. Gao, and H. Xu, “Adaptive denoising for network traffic measurement,” IEEE Transactions on Network Science and Engineering, 2025.

[2] H. Huang, Y.-E. Sun, C. Ma, S. Chen, Y. Du, H. Wang, and Q. Xiao, “Spread estimation with non-duplicate sampling in high-speed networks,” IEEE/ACM Transactions on Networking, vol. 29, no. 5, pp. 2073–2086, 2021.

[3] Q. Huang et al., “Sketchvisor: Robust network measurement for software packet processing,” in ACM SIGCOMM, 2017, pp. 113–126.

[4] X. Chen, Q. Huang, P. Wang, H. Liu, Y. Chen, D. Zhang, H. Zhou, and C. Wu, “Mtp: Avoiding control plane overload with measurement task placement,” in IEEE INFOCOM, 2021, pp. 1–10.

[5] R. Ben Basat et al., “Pint: Probabilistic in-band network telemetry,” in ACM SIGCOMM, 2020, pp. 662–680.

[6] S. Sheng, Q. Huang, and P. P. Lee, “Deltaint: Toward general in-band network telemetry with extremely low bandwidth overhead,” in IEEE ICNP, 2021, pp. 1–11.

[7] Y. Li, R. Miao, C. Kim, and M. Yu, “Flowradar: a better netflow for data centers,” in USENIX NSDI, 2016, pp. 311–324.

[8] T. Yang et al., “Elastic sketch: Adaptive and fast network-wide measurements,” in ACM SIGCOMM, 2018, pp. 561–575.

[9] Q. Huang, P. P. Lee, and Y. Bao, “Sketchlearn: relieving user burdens in approximate measurement with automated statistical inference,” in ACM SIGCOMM, 2018, pp. 576–590.

[10] Z. Liu et al., “One sketch to rule them all: Rethinking network flow monitoring with univmon,” in ACM SIGCOMM, 2016, pp. 101–114.

[11] Q. Huang et al., “Toward nearly-zero-error sketching via compressive sensing,” in USENIX NSDI, 2021, pp. 1027–1044.

[12] Z. Liu et al., “Nitrosketch: Robust and general sketch-based monitoring in software switches,” in ACM SIGCOMM, 2019, pp. 334–350.

[13] Y. Zhang, Z. Liu, R. Wang et al., “Cocosketch: high-performance sketch-based measurement over arbitrary partial key query,” in ACM SIGCOMM, 2021, pp. 207–222.

[14] H. Namkung et al., “Sketchlib: Enabling efficient sketch-based monitoring on programmable switches,” in USENIX NSDI, 2022, pp. 1–17.

[15] N. Handigol, B. Heller, V. Jeyakumar, D. Mazieres, and N. McKeown,\` “I know what your packet did last hop: Using packet histories to troubleshoot networks,” in USENIX NSDI, 2014, pp. 71–85.

[16] T. Pan, E. Song, Z. Bian, X. Lin, X. Peng, J. Zhang, T. Huang, B. Liu, and Y. Liu, “Int-path: Towards optimal path planning for inband network-wide telemetry,” in IEEE INFOCOM, 2019, pp. 487–495.

[17] Y. Zhu et al., “Packet-level telemetry in large datacenter networks,” in ACM SIGCOMM, 2015, pp. 479–491.

[18] K. Yang, S. Long, Q. Shi, Y. Li, Z. Liu, Y. Wu, T. Yang, and Z. Jia, “Sketchint: Empowering int with towersketch for per-flow per-switch measurement,” IEEE Transactions on Parallel and Distributed Systems, vol. 34, no. 11, pp. 2876–2894, 2023.

[19] Y. Zhao et al., “Lightguardian: A full-visibility, lightweight, in-band telemetry system using sketchlets,” in USENIX NSDI, 2021, pp. 991– 1010.

[20] T. Yang, Y. Zhou, H. Jin, S. Chen, and X. Li, “Pyramid sketch: A sketch framework for frequency estimation of data streams,” Proceedings of the VLDB Endowment, vol. 10, no. 11, pp. 1442–1453, 2017.

[21] A. Roy, H. Zeng, J. Bagga, G. Porter, and A. C. Snoeren, “Inside the social network’s (datacenter) network,” in ACM SIGCOMM, 2015, pp. 123–137.

[22] CAIDA Traces, http://www.caida.org/data/overview/.

[23] T. Benson, A. Akella, and D. A. Maltz, “Network traffic characteristics of data centers in the wild,” in ACM IMC, 2010, pp. 267–280.

[24] Tofino2. https://www.intel.com/content/www/us/en/products/networkio/programmable-ethernet-switch/tofino-2-series.html.

[25] A. Anup, L. Zaoxing, and S. Srinivasan, “Heterosketch: Coordinating network-wide monitoring in heterogeneous and dynamic networks,” in USENIX NSDI, 2022, pp. 1–23.

[26] J. Liu, R. B. Basat, L. De Wardt, H. Dai, and G. Chen, “Disco: A dynamically configurable sketch framework in skewed data streams,” in IEEE ICDE, 2024, pp. 4801–4814.

[27] W. Wu, Z. Li, X. Liu, Z. Wang, H. Pan, G. Zhang, and G. Xie, “Lemon: Network-wide ddos detection with routing-oblivious per-flow measurement,” in USENIX Security, 2025.

[28] G. Cormode and S. Muthukrishnan, “What’s new: Finding significant differences in network data streams,” IEEE/ACM Transactions on Net-

working, vol. 13, no. 6, pp. 1219–1232, 2005.

[29] M. Charikar et al., “Finding frequent items in data streams,” Theoretical Computer Science, vol. 312, no. 1, pp. 3–15, 2004.

[30] A. Gupta, R. Harrison, M. Canini, N. Feamster, J. Rexford, and W. Willinger, “Sonata: Query-driven streaming network telemetry,” in ACM SIGCOMM, 2018, pp. 357–371.

[31] F. Li, Y. Lv, Y. Yan, C. Gao, X. Wang, and J. Cao, “Learningbased sketch for adaptive and high-performance network measurement,” IEEE/ACM Transactions on Networking, 2024.

[32] Z. Liu, H. Namkung et al., “Jaqen: A high-performance switch-native approach for detecting and mitigating volumetric ddos attacks with programmable switches,” in USENIX Security, 2021.

[33] Int protocol. https://github.com/p4lang/p4-applications/blob/ master/docs/telemetry report.pdf.

[34] S. Tang, D. Li, B. Niu, J. Peng, and Z. Zhu, “Sel-int: A runtimeprogrammable selective in-band network telemetry system,” IEEE transactions on network and service management, vol. 17, no. 2, pp. 708–721, 2019.

[35] D. Suh, S. Jang, S. Han, S. Pack, and X. Wang, “Flexible sampling-based in-band network telemetry in programmable data plane,” ICT Express, vol. 6, no. 1, pp. 62–65, 2020.

[36] Y. Kim, D. Suh, and S. Pack, “Selective in-band network telemetry for overhead reduction,” in IEEE CloudNet, 2018, pp. 1–3.

[37] Gurobi Optimizer, http://www.gurobi.com.

[38] CPLEX, https://www.ibm.com/analytics/cplex-optimizer.

[39] sflow. http://sflow.org/about/index.php.

[40] Netflow. https://www.ietf.org/rfc/rfc3954.txt.

[41] J. Achiam, D. Held, A. Tamar, and P. Abbeel, “Constrained policy optimization,” in International conference on machine learning. PMLR, 2017, pp. 22–31.

[42] Pytorch. https://pytorch.org/.

[43] X. Chen et al., “Speed: Resource-efficient and high-performance deployment for data plane programs,” in IEEE ICNP, 2020, pp. 1–12.

[44] J. Gao, E. Zhai, H. H. Liu et al., “Lyra: A cross-platform language and compiler for data plane programming on heterogeneous asics,” in ACM SIGCOMM, 2020, pp. 435–450.

[45] PktGen, https://pktgen-dpdk.readthedocs.io/.

[46] L. Jose, L. Yan et al., “Compiling packet programs to reconfigurable switches.” in USENIX NSDI, 2015, pp. 103–115.

[47] X. Chen, Q. Xiao, H. Liu, Q. Huang, D. Zhang, X. Liu, L. Hu, H. Zhou, C. Wu, and K. Ren, “Eagle: Toward scalable and near-optimal networkwide sketch deployment in network measurement,” in ACM SIGCOMM, 2024, pp. 291–310.

[48] S. Knight et al., “The internet topology zoo,” IEEE Journal on Selected Areas in Communications, vol. 29, no. 9, pp. 1765–1775, 2011.

[49] Data-center switch silicon developments keep the market future-proof, https://tinyurl.com/2782xsh3.

[50] B. Heller, R. Sherwood, and N. McKeown, “The controller placement problem,” ACM SIGCOMM Computer Communication Review, vol. 42, no. 4, pp. 473–478, 2012.

[51] G. Cormode and S. Muthukrishnan, “An improved data stream summary: the count-min sketch and its applications,” Journal of Algorithms, vol. 55, no. 1, pp. 58–75, 2005.

[52] H. Liu, X. Chen, Q. Huang, D. Kong, J. Sun, D. Zhang, H. Zhou, and C. Wu, “Escala: Timely elastic scaling of control channels in network measurement,” in IEEE INFOCOM, 2022, pp. 1848–1857.

[53] L. Tang et al., “Mv-sketch: A fast and compact invertible sketch for heavy flow detection in network data streams,” in IEEE INFOCOM, 2019, pp. 2026–2034.

[54] Y. Li et al., “Hpcc: High precision congestion control,” in ACM SIGCOMM, 2019, pp. 44–58.

[55] M. Alizadeh et al., “Data center tcp (dctcp),” in ACM SIGCOMM, 2010, pp. 63–74.

[56] R. Joshi, T. Qu, M. C. Chan, B. Leong, and B. T. Loo, “Burstradar: Practical real-time microburst monitoring for datacenter networks,” in APSys, 2018, pp. 1–8.