# Pruned Traffic Trees: Native Semantic Compression with a Protocol-Structured Model Family for Encrypted Traffic Classification

Yuantu Luo<sup>∗</sup>, Jun Tao<sup>∗</sup>, Xiangyu Xu<sup>†</sup>, Linxiao Yu<sup>∗</sup>, Kangying Li<sup>∗</sup>

School of Cyber Science and Engineering, Southeast University, Nanjing, China

{ytluo, juntao, yulinxiaoybbb, kangying}@seu.edu.cn

<sup>†</sup> School of Computer Science and Engineering, Southeast University, Nanjing, China xy-xu@seu.edu.cn

Abstract—Deep learning has achieved strong performance in encrypted traffic classification (ETC), yet its computational cost limits deployment on resource-constrained network devices such as routers and middleboxes. Existing compression methods mainly operate on weights, channels, hidden representations, or predictions, but do not explicitly determine which protocol fields and structural contexts should remain. We propose Pruned Traffic Trees (PTT), a three-level protocol-structured model family that treats native protocol structures as compression units. PTT-Full learns protocol-structured representations and field salience from complete Protocol Tree Graphs (PTGs), with flowlevel self-supervised learning and protocol-presence-aware sparse execution. The learned salience and TopK+k closure construct Distilled PTGs (PTG-Ds) for PTT-Distilled, while PTT-Lite inherits this topology and reduces width through structure-aligned transfer and flow-level logits distillation. Under flow-disjoint and Strong Information Information (SII)-masked settings, PTT-Full achieves Macro-F1 scores of 0.9519 and 0.9416 on CSTNET-TLS1.3 and CipherSpectrum, while PTT-Lite retains 0.9325 and 0.9136 with 80.3% and 61.3% fewer parameters, 98.85% and 98.78% lower effective GFLOPs, and 8.75× and 8.46× CPU inference speedups. These results demonstrate that treating protocol structure itself as the compression object enables effective performance-efficiency trade-offs for lightweight ETC.

Index Terms—Encrypted Traffic Classification, Protocol-Structured Representation, Semantic Compression, Sparse Expert Model

## I. INTRODUCTION

Encrypted payloads obscure application content, forcing encrypted traffic classification (ETC) models to rely on the structural evidence that remains observable at network devices [1]. Packet dissection exposes protocol fields, their boundaries, and their positions in the protocol hierarchy, which are interpreted jointly rather than as isolated bytes during traffic analysis. Together, these properties make protocol fields natural semantic units for ETC: they support structure-aware representation and, unlike anonymous bytes or latent channels, can be explicitly retained or removed during compression. A field’s meaning depends on both its value and structural position, making field identity and protocol context inseparable. This suggests that ETC models should preserve protocol fields as persistent units throughout both representation learning and compression.

Existing ETC methods commonly encode traffic using packet-direction and timing sequences [2]–[5], raw-byte or token sequences [6], [7], or image-like representations [8], [9]. These representations can achieve strong classification performance, but they do not explicitly preserve protocoldefined field boundaries and parent–child relations. Fixedlength processing may further introduce padding or truncation, which inserts artificial values or removes useful traffic information. Generic graph-based methods improve structural modeling, but their edges are often constructed from statistical or heuristic relations rather than the native hierarchy produced by packet dissection [10]. Consequently, protocol fields are rarely exposed as persistent, semantically identifiable units that can later be selected or removed during model compression.

Beyond representation accuracy, practical ETC deployment should satisfy the latency, memory, and computation budgets of routers and middleboxes. Existing lightweight designs typically compress models through pruning, quantization, width reduction, or knowledge distillation [11]. These methods operate mainly on weights, channels, hidden representations, or predictions, and therefore do not explicitly control which protocol evidence remains available to a compact classifier. Applying structure pruning directly to a graph does not fully resolve this issue either: independently retained nodes may become detached from the protocol paths that define their context. This suggests that lightweight ETC requires more than a smaller neural network. The representation itself should expose semantically meaningful units that can be removed while retaining the protocol context required by the remaining fields. In other words, compression should answer both what protocol evidence to retain and how to retain it in a valid structural context.

To address these challenges, we present Pruned Traffic Trees (PTT), a protocol-structured ETC model family built on Protocol Tree Graphs (PTGs) [12]. PTGs align parsed protocol fields and their parent–child relations with persistent graph nodes and edges. While the inherited PTG representation uses this structure for representation learning, PTT further turns its field-level alignment into an explicit compression interface. PTT-Full learns protocol-structured representations together with field salience from complete PTGs. The learned salience determines which fields are retained, while TopK+k closure restores their required protocol paths to construct compact Distilled PTGs (PTG-Ds) and instantiate PTT-Distilled. PTT-Lite then inherits the compressed topology and reduces width through structure-aligned transfer and flow-level logits distillation. To ensure that the measured gains reflect transferable traffic patterns rather than shortcut indicators or flow leakage, all methods are evaluated under SII-masked [13] and flowdisjoint settings [14].

Different from model-level compression that operates on anonymous parameters or latent channels, PTT makes protocol fields and their native hierarchy explicit objects of compression. Overall, our contributions are summarized as follows:

• We propose PTG-native structural compression, which turns field-aligned PTGs into an explicit compression interface. Learned field salience determines which protocol fields are retained, while TopK+k closure constructs the minimal hierarchy-closed PTG containing those fields. This reduces graph structure without breaking the native protocol context of the retained evidence.

• We develop PTT-Full as the high-capacity source model. It combines flow-level self-supervised learning with protocol-presence-aware sparse dispatch, executing experts only for present protocol components and converting protocol absence into inference acceleration.

• We derive PTT-Lite from PTT-Distilled through structure-aligned width transfer and flow-level logits distillation. Experiments on two TLS 1.3 datasets under flow-disjoint and SII-masked settings show that the PTT variants provide strong performance–resource trade-offs.

## II. RELATED WORK

a) Encrypted Traffic Representation and Classification: Encrypted traffic classifiers encode flows as images [8], [9], raw-byte or token sequences [3], [4], [15], packet-length and timing sequences [2], [7], or multi-level features [5], [16]. Recent sequence models improve byte-level learning through joint byte–label attention or large-scale traffic pretraining [17]. Graph methods capture packet-, message-, or feature-level interactions [18], while PTGAMoE aligns graph nodes and edges with parsed fields and their native hierarchy [12]. However, these representations either flatten protocol evidence into implicit features or model generic interactions without exposing protocol fields as explicit structural units for compression. Moreover, shortcut features and improper splitting can substantially inflate ETC results [13], [14].

b) Knowledge Distillation and Lightweight Traffic Analysis: Existing lightweight traffic analysis mainly follows general model compression paradigms, including knowledge distillation, pruning, and representation reduction. Graph distillation transfers logits [19]–[21], embeddings [22]–[24], cross-layer relations [25], or neighborhood information to compact students [26], [27]. Other lightweight traffic studies explore programmable-switch deployment, sample-efficient learning, graph cross-distillation, and contextual masking distillation [28]–[31]. However, these methods mainly compress model parameters or representations rather than explicitly preserving the protocol context of retained fields. Moreover, they neither select the protocol evidence to retain nor preserve its native hierarchy.

c) Mixture of Experts for Traffic Analysis: Sparse Mixture-of-Experts (MoE) models improve capacity– computation trade-offs through conditional expert activation [32], [33]. Recent traffic models use experts for sparse foundation modeling, heterogeneous traffic specialization, and multi-view fusion [34]–[36]. However, their routing decisions are typically defined over learned tokens, modalities, or predefined branches, rather than protocol components physically present in each packet.

PTT differs by treating parsed fields and their hierarchy as explicit semantic units for both sparse execution and compression. It leverages protocol presence as an explicit routing signal and further uses learned field salience to guide hierarchy-preserving protocol compression.

## III. PROTOCOL-STRUCTURED SOURCE MODEL PTT-FULL

As shown in Fig. 1, building on the Protocol Tree Graph (PTG) representation [12] and graph-expert backbone, PTT-Full adds flow-level self-supervised learning and protocolpresence-aware sparse dispatch.

## A. Graph-Based Expert Backbone

Let $\boldsymbol { \mathcal { D } } = \{ ( F _ { i } , y _ { i } ) \} _ { i = 1 } ^ { N }$ be a labeled ETC dataset, where $F _ { i } ~ = ~ ( p _ { i , 1 } , \dots , p _ { i , T _ { i } } )$ is a flow and $y _ { i }$ is its class. For a maximum of $P$ packets per flow, $T _ { i } = \mathrm { m i n } ( N _ { i } , P ) $ retains the first packets in capture order.

Each packet is represented over an expert-indexed PTG set $\{ { \mathcal G } _ { F , e } \mid e \in { \mathcal E } \}$ . For expert $e ,$ the fixed Full schema is

$$
\mathcal {G} _ {F, e} = (\mathcal {V} _ {F, e}, \mathcal {E} _ {F, e}),\tag{1}
$$

$$
\mathcal {V} _ {F, e} = \mathcal {V} _ {F, e} ^ {\text { real }} \cup \mathcal {V} _ {F, e} ^ {\text { abs }},\tag{2}
$$

$$
\mathcal {E} _ {F, e} = \mathcal {E} _ {F, e} ^ {\text { hier }} \cup \mathcal {E} _ {F, e} ^ {\text { sink }}.\tag{3}
$$

Here, $\mathcal { V } _ { F , e } ^ { \mathrm { r e a l } }$ contains real protocol-field nodes whose values are obtained from packet dissection, whereas $\gamma _ { F , e } ^ { \mathrm { a b s } }$ contains abstract schema nodes used to preserve the protocol hierarchy. $\mathcal { E } _ { F , e } ^ { \mathrm { h i e r } }$ contains undirected hierarchical edges induced by the parent–child relations of packet dissection, while $\mathcal { E } _ { F , e } ^ { \mathrm { s i n k } }$ connects schema nodes with the layer-wise sink node used for graph readout. Each PTG is conceptually undirected. In implementation, every undirected edge is represented by two directed edges for bidirectional GAT message passing.

For packet $p _ { i , t } , \mathbf { X } _ { i , t , e } \in \mathbb { R } ^ { | \mathcal { V } _ { F , e } | \times d _ { F } }$ contains node representations in the fixed schema order. Each node v has a shared gate logit $\alpha _ { e , v }$ and activation

$$
s _ {e, v} = \sigma (\alpha_ {e, v}), \qquad 0 <   s _ {e, v} <   1.\tag{4}
$$

The gated node representations and expert output are

$$
\widetilde {\mathbf {X}} _ {i, t, e} = [ s _ {e, v} \mathrm{LN} (\mathbf {x} _ {i, t, e, v}) ] _ {v \in \mathcal {V} _ {F, e}},
$$

$$
\mathbf {h} _ {i, t, e} = f _ {e} (\widetilde {\mathbf {X}} _ {i, t, e}, \mathcal {E} _ {F, e}; \theta_ {F, e}), \qquad \mathbf {h} _ {i, t, e} \in \mathbb {R} ^ {d _ {F}}.\tag{5}
$$

![](images/c9cb7c7fae88da35779aadc9ef3050f69173c7c9bb8d00206cb9e465af558c7e.jpg)  
Fig. 1: Overview of PTT-Full and its flow-level learning pipeline.

Here, $f _ { e }$ is a two-layer graph attention encoder followed by mean readout:

$$
\begin{array}{r l} & {\mathbf {Z} _ {i, t, e} ^ {(0)} = \mathrm{Dropout} (\widetilde {\mathbf {X}} _ {i, t, e}),} \\ & {\mathbf {Z} _ {i, t, e} ^ {(1)} = \mathrm{ELU} \left(\mathrm{GAT} _ {e} ^ {(1)} (\mathbf {Z} _ {i, t, e} ^ {(0)}, \mathcal {E} _ {F, e})\right),} \\ & {\mathbf {Z} _ {i, t, e} ^ {(2)} = \mathrm{GAT} _ {e} ^ {(2)} (\mathbf {Z} _ {i, t, e} ^ {(1)}, \mathcal {E} _ {F, e}),} \\ & {\mathbf {h} _ {i, t, e} = \mathrm{MeanPool} (\mathbf {Z} _ {i, t, e} ^ {(2)}).} \end{array}\tag{6}
$$

The first layer uses multi-head attention and concatenation, while the second outputs dimension $d _ { F }$ . The learned real-node gates provide field salience for structural compression.

Beyond the PTG schema and its corresponding graphexpert architecture, we introduce flow batching with variable lengths, flow-level self-supervised learning, and protocolpresence-aware sparse execution in PTT-Full to enhance the traffic representation.

## B. Protocol-Presence-Aware Sparse MoE

a) Flow-Centric Batching: To train and evaluate PTT at the flow granularity, packets from the same flow are first organized into a variable-length micro-batch. The packet indices of flow i form the micro-batch

$$
\mathcal {I} _ {i} ^ {\mathrm{pkt}} = \{(i, t) \mid 1 \leq t \leq T _ {i} \}.\tag{7}
$$

For each optimization step, the sampler selects up to $N _ { B }$ flows with index set $\mathcal { T } _ { B } ^ { \mathrm { f l o w } }$ and concatenates their variable-length packet sets into a macro-batch:

$$
\mathcal {I} _ {\mathcal {B}} ^ {\mathrm{pkt}} = \bigcup_ {i \in \mathcal {I} _ {\mathcal {B}} ^ {\mathrm{flow}}} \mathcal {I} _ {i} ^ {\mathrm{pkt}}, \qquad | \mathcal {I} _ {\mathcal {B}} ^ {\mathrm{pkt}} | \leq N _ {\mathcal {B}} P.\tag{8}
$$

This macro-batch introduces no packet padding, and flow identifiers are retained to regroup packet outputs for flow-level learning.

b) Protocol Presence: A packet should not invoke an expert for a protocol component that it does not contain. For packet $p _ { i , t }$ and expert $e ,$ define

$$
\begin{array}{l} \mathcal {P} _ {i, t, e} = \{v \in \mathcal {V} _ {F, e} ^ {\text {real}} \mid v \text {is observed in} p _ {i, t} \}, \\ m _ {i, t, e} = \mathbb {I} [ \mathcal {P} _ {i, t, e} \neq \varnothing ]. \end{array}\tag{9}
$$

For the TCP-based flows considered here, IP and TCP-core experts are retained as structural anchors:

$$
\begin{array}{r l} & {\mathcal {E} _ {\mathrm{anchor}} = \{e _ {\mathrm{IP}}, e _ {\mathrm{TCPcore}} \},} \\ & {m _ {i, t, e} ^ {\prime} = \max (m _ {i, t, e}, \mathbb {I} [ e \in \mathcal {E} _ {\mathrm{anchor}} ]).} \end{array}\tag{10}
$$

where I[·] denotes the indicator function. The active packet indices of expert e are gathered into an expert-specific subbatch

$$
\mathcal {I} _ {\mathcal {B}, e} ^ {\mathrm{act}} = \{(i, t) \in \mathcal {I} _ {\mathcal {B}} ^ {\mathrm{pkt}} \mid m _ {i, t, e} ^ {\prime} = 1 \}.\tag{11}
$$

Thus, protocol presence determines whether an expert can execute, while the fusion gate below determines how much its output contributes.

c) Sparse Dispatch and Fusion: Masking an expert only after its forward pass does not reduce computation. PTT-Full therefore uses a gather–execute–scatter procedure: active packets are gathered into expert-specific sub-batches, each nonempty encoder executes once, and its outputs are scattered back to the original packet positions. In particular,

$$
\mathcal {I} _ {\mathcal {B}, e} ^ {\text { act }} = \varnothing \quad \Longrightarrow \quad f _ {e} \text {   is   not   executed. }\tag{12}
$$

Inactive positions are zero-filled:

$$
\overline {{\mathbf {h}}} _ {i, t, e} = \left\{ \begin{array}{l l} \mathbf {h} _ {i, t, e}, & m _ {i, t, e} ^ {\prime} = 1, \\ \mathbf {0}, & m _ {i, t, e} ^ {\prime} = 0. \end{array} \right.\tag{13}
$$

Given expert order $( e _ { 1 } , \ldots , e _ { | \varepsilon | } )$ , cooperative fusion is

$$
\begin{array}{r l} & {\beta_ {i, t} = \mathrm{MLP} _ {g} (\overline {{\mathbf {h}}} _ {i, t, e _ {1}} \| \dots \| \overline {{\mathbf {h}}} _ {i, t, e _ {| \mathcal {E} |}}),} \\ & {g _ {i, t, e} = m _ {i, t, e} ^ {\prime} \sigma (\beta_ {i, t, e}),} \\ & {\mathbf {z} _ {i, t} = \sum_ {e \in \mathcal {E}} g _ {i, t, e} \overline {{\mathbf {h}}} _ {i, t, e}.} \end{array}\tag{14}
$$

Unlike competitive softmax routing, sigmoid fusion allows coexisting components such as IP, TCP, and TLS to contribute simultaneously.

## C. Flow-Level Pretraining and Classification

Packets from the same flow describe one communication process. PTT-Full therefore defines contrastive relations at the flow level rather than treating packets as independent samples. During pretraining, two views perturb node observations and selected auxiliary sink edges while sharing the canonical PTGs, expert assignments, and presence masks. These temporary perturbations do not change the schemas later used for compression.

The sparse backbone produces packet representations $\mathbf { z } _ { i , t } ^ { ( 1 ) }$ and $\mathbf { z } _ { i , t } ^ { ( 2 ) }$ . They are pooled within each flow:

$$
\begin{array}{l} \mathbf {r} _ {i} ^ {(\xi)} = \underset {(i, t) \in \mathcal {I} _ {i} ^ {\mathrm{pkt}}} {\text {MaxPool}} \mathbf {z} _ {i, t} ^ {(\xi)}, \qquad \xi \in \{1, 2 \}, \\ \mathcal {L} _ {\text {SSL}} = \text {NTXent} \left(\{\mathbf {r} _ {i} ^ {(1)}, \mathbf {r} _ {i} ^ {(2)} \mid i \in \mathcal {I} _ {\mathcal {B}} ^ {\text {flow}} \}\right). \end{array}\tag{15}
$$

Here, NTXent denotes the normalized temperature-scaled cross-entropy (NT-Xent) loss. The two views of the same flow form a positive pair, while representations from other flows in the macro-batch form negatives. Packets from the same flow are never treated as negatives.

For supervised adaptation, the pretrained backbone is jointly fine-tuned with a classifier:

$$
\boldsymbol {\ell} _ {i, t} = \operatorname{MLP} _ {c} (\mathbf {z} _ {i, t}), \quad \boldsymbol {\ell} _ {i, t} \in \mathbb {R} ^ {C}.\tag{16}
$$

Packet logits are averaged within each flow:

$$
\overline {{\ell}} _ {i} = \frac {1}{T _ {i}} \sum_ {(i, t) \in \mathcal {I} _ {i} ^ {\mathrm{pkt}}} \ell_ {i, t}.\tag{17}
$$

The supervised objective is

$$
\mathcal {L} _ {\text { Full }} ^ {(\sup)} = \mathbb {E} _ {(F _ {i}, y _ {i}) \sim \widehat {\mathcal {D}} _ {\text { tr }}} \left[ \mathrm{CE} (\overline {{\ell}} _ {i}, y _ {i}) \right],\tag{18}
$$

where CE denotes the cross-entropy loss, and $\begin{array} { r l } { \widehat { y } _ { i } } & { { } = } \end{array}$ arg max $\boldsymbol { \cdot } \bar { \boldsymbol { \ell } } _ { i , c }$ at inference.

Let $\theta _ { F } ^ { * }$ be the optimized parameters and

$$
\begin{array}{c} \mathcal {G} _ {F} = \{\mathcal {G} _ {F, e} \mid e \in \mathcal {E} \}, \\ M _ {F} = (\theta_ {F} ^ {*}, \mathcal {G} _ {F}, d _ {F}). \end{array}\tag{19}
$$

The trained PTT-Full serves as both the high-capacity classifier and the source of field salience, PTG structure, and parameters for compression.

## IV. PTG-NATIVE STRUCTURAL COMPRESSION

Sparse dispatch skips absent experts, but each active expert still processes a complete PTG. As shown in Fig. 2, PTT-Distilled compresses these PTGs by selecting salient fields and applying TopK+k closure to preserve their structural context, while PTT-Lite inherits the compressed topology and further reduces representation width.

![](images/0e1dbeb6ee457d33b72d1530411f66e227c377e6950a3a8209b4f8be9063a4e2.jpg)  
Fig. 2: PTG-native structural compression from PTT-Full to PTT-Distilled and PTT-Lite.

## A. PTT-Full to PTT-Distilled

a) Gate-Derived Field Salience: The gates learned by PTT-Full provide a shared salience score for each real protocol field. For expert e, the candidate set is

$$
\mathcal {C} _ {e} = \mathcal {V} _ {F, e} ^ {\mathrm{real}}.\tag{20}
$$

We normalize the trained gates within each expert to obtain Normalized Field Salience (NFS):

$$
\mathrm{NFS} _ {e} (v) = \frac {s _ {e , v} ^ {*}}{\sum_ {u \in \mathcal {C} _ {e}} s _ {e , u} ^ {*}}, \qquad v \in \mathcal {C} _ {e}.\tag{21}
$$

NFS expresses the learned gate values on a relative scale within each expert and is used only for field ranking. Unlike causal attribution methods, NFS is designed as a compressionoriented criterion. Its validity is evaluated by whether the resulting protocol-closed subgraphs preserve classification performance under matched compression budgets. Given a perexpert budget K, we construct the Top-K salience set as:

$$
\begin{array}{l} K _ {e} = \min (K, | \mathcal {C} _ {e} |), \\ \mathcal {S} _ {e} ^ {K} = \mathrm{TopK} _ {v \in \mathcal {C} _ {e}} (\mathrm{NFS} _ {e} (v), K _ {e}). \end{array}\tag{22}
$$

b) TopK+k PTG Closure: Retaining the Top-K fields answers what evidence should be preserved, but not how these fields remain meaningful after compression. We therefore design TopK+k closure to restore the minimal protocol hierarchy required by these fields.

Although the PTG is undirected, its hierarchical edges retain the parent–child provenance inherited from packet dissection. We represent this provenance by $\mathrm { P a r } _ { F , e } ( v )$ , the parent set of node v in the original protocol hierarchy. As shown in Algorithm 1, starting from $\bar { S } _ { e } ^ { K }$ , PTT recursively follows these parent relations until all required ancestors are retained. Let V<sup>core</sup> denote the selected fields together with the PTG schema nodes recovered by this closure.

The additional closure size is

$$
k _ {e} = | \mathcal {V} _ {e} ^ {\mathrm{core}} \setminus \mathcal {S} _ {e} ^ {K} |, \qquad | \mathcal {V} _ {e} ^ {\mathrm{core}} | = K _ {e} + k _ {e}.\tag{23}
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: TopK+k PTG Closure

Input: Full PTGs  $\{G_{F,e}\}_{e\in\varepsilon}$ ; parent maps  $\{Par_{F,e}\}_{e\in\varepsilon}$ ; selected field sets  $\{S_{e}^{K}\}_{e\in\varepsilon}$ 

Output: Distilled PTGs  $G_{D}$ ; closure sizes  $\{k_{e}\}_{e\in\varepsilon}$ 

1  $G_{D} \leftarrow \varnothing;$ 

2 foreach  $e \in E$  do

3  $V_{e}^{core} \leftarrow S_{e}^{K};$ 

4  $Q_{e} \leftarrow S_{e}^{K};$ 

5 while  $Q_{e} \neq \varnothing$  do

6 select and remove one node v from  $Q_{e}$ ;

7 foreach  $u \in Par_{F,e}(v)$  do

8 if  $u \notin V_{e}^{core}$  then

9  $V_{e}^{core} \leftarrow V_{e}^{core} \cup \{u\};$ 

10  $Q_{e} \leftarrow Q_{e} \cup \{u\};$ 

11 end

12 end

13 end

14  $k_{e} \leftarrow |V_{e}^{core} \setminus S_{e}^{K}|;$ 

15  $V_{D,e} \leftarrow V_{e}^{core} \cup \{v_{F,e}^{sink}\};$ 

16  $E_{D,e}^{hier} \leftarrow \{(u,v) \in E_{F,e}^{hier} \mid u,v \in V_{e}^{core}\};$ 

17  $E_{D,e}^{sink} \leftarrow \{(v,v_{F,e}^{sink}) \mid v \in V_{e}^{core}\};$ 

18  $E_{D,e} \leftarrow E_{D,e}^{hier} \cup E_{D,e}^{sink};$ 

19  $G_{D,e} \leftarrow (V_{D,e}, E_{D,e});$ 

20  $G_{D} \leftarrow G_{D} \cup \{G_{D,e}\};$ 

21 end

22 return  $G_{D}, \{k_{e}\}_{e\in\varepsilon};$
</div>

The auxiliary sink is added only to preserve the global aggregation structure of the PTG and does not contribute to $k _ { e } ,$ giving $| \mathcal { V } _ { D , e } | = K _ { e } + k _ { e } + 1$

Ignoring the auxiliary sink node, $\mathcal { V } _ { e } ^ { \mathrm { c o r e } }$ is the unique minimal hierarchy-preserving node set that contains $\bar { S _ { e } ^ { K } }$ and is closed under the parent relation inherited from the original protocol hierarchy. Any smaller node set would necessarily remove either a selected field or an ancestor required by one of its original protocol paths. The value of $k _ { e }$ is therefore determined by the protocol paths of the selected fields rather than by a fixed pruning ratio.

Since $\mathcal { V } _ { e } ^ { \mathrm { c o r e } }$ prevents a node from being enqueued more than once, the ancestor traversal visits each discovered node once. Constructing $\mathcal { E } _ { D , e } ^ { \mathrm { h i e r } }$ requires one scan of the Full hierarchical edge set, giving an overall complexity of $\mathcal { O } ( | \mathcal { V } _ { F , e } | + | \mathcal { E } _ { F , e } ^ { \mathrm { h i e r } } | )$ for each expert.

c) Structure-Aligned Projection: The PTG-D topology is fixed before parameter projection. For $d _ { D } < d _ { F }$ , the Distilled model is initialized as

$$
\begin{array}{r} \theta_ {D} ^ {(0)} = \Pi_ {F \to D} (\theta_ {F} ^ {*}; \mathcal {G} _ {D}), \\ M _ {D} ^ {(0)} = (\theta_ {D} ^ {(0)}, \mathcal {G} _ {D}, d _ {D}). \end{array}\tag{24}
$$

Here, $\Pi _ { F  D }$ denotes structure-aligned channel selection. Specifically, Π $F  D$ selects the $\mathrm { t o p } { \cdot } d _ { D }$ channels by aggregated squared-ℓ<sub>2</sub> weight magnitude and slices them consistently across aligned model modules, while retained PTG nodes are matched by protocol-field name. The model is then adapted with flow-level supervision:

$$
\begin{array}{c} \mathcal {L} _ {\text {Distilled}} ^ {(\sup)} = \mathbb {E} _ {(F _ {i}, y _ {i}) \sim \widehat {\mathcal {D}} _ {\mathrm{tr}}} [ \mathrm{CE} (\overline {{\ell}} _ {D, i}, y _ {i}) ], \\ \theta_ {D} ^ {*} = \arg \min _ {\theta_ {D}} \mathcal {L} _ {\text {Distilled}} ^ {(\sup)}, \\ M _ {D} = (\theta_ {D} ^ {*}, \mathcal {G} _ {D}, d _ {D}). \end{array}\tag{25}
$$

PTT-Distilled retains the expert set, anchor experts, and sparse dispatch rule of PTT-Full, but each active expert processes a smaller graph.

## B. PTT-Distilled to PTT-Lite

Unlike the previous stage, this stage removes no protocol field. PTT-Lite keeps $\mathcal { G } _ { D }$ unchanged and only reduces representation width from $d _ { D }$ to $d _ { L } < d _ { D }$

a) Width Transfer and Adaptation: Because PTT-Distilled and PTT-Lite share the same PTG-D schemas and expert organization, their node-specific parameters are structurally aligned:

$$
\begin{array}{r} \theta_ {L} ^ {(0)} = \Pi_ {D \to L} (\theta_ {D} ^ {*}; \mathcal {G} _ {D}), \\ M _ {L} ^ {(0)} = (\theta_ {L} ^ {(0)}, \mathcal {G} _ {D}, d _ {L}). \end{array}\tag{26}
$$

$\Pi _ { D  L }$ applies the same criterion to select the top $\cdot d _ { L }$ channels and slices the corresponding dimensions consistently across all aligned modules. The projected experts are briefly frozen while the narrower fusion and classifier adapt to the new feature space. All parameters are then jointly fine-tuned using

$$
\mathcal {L} _ {\mathrm{Lite}} ^ {(\mathrm{sup})} = \mathbb {E} _ {(F _ {i}, y _ {i}) \sim \widehat {\mathcal {D}} _ {\mathrm{tr}}} [ \mathrm{CE} (\overline {{\ell}} _ {L, i}, y _ {i}) ].\tag{27}
$$

b) Flow-Level Logits Distillation: Because the Lite model has lower capacity, it is additionally guided by the flowlevel predictions of PTT-Distilled. With temperature $\tau _ { \mathrm { K D } }$

$$
q _ {X} (c \mid F _ {i}) = \frac {\exp (\overline {{\ell}} _ {X , i} ^ {c} / \tau_ {\mathrm{KD}})}{\sum_ {c ^ {\prime} = 1} ^ {C} \exp (\overline {{\ell}} _ {X , i} ^ {c ^ {\prime}} / \tau_ {\mathrm{KD}})}, \qquad X \in \{D, L \}.\tag{28}
$$

The Distilled teacher is fixed during Lite adaptation, and

$$
\mathcal {L} _ {\mathrm{KD}} = \tau_ {\mathrm{KD}} ^ {2} \mathbb {E} _ {F _ {i} \sim \widehat {\mathcal {D}} _ {\mathrm{tr}}} \left[ \mathrm{KL} (q _ {D} (\cdot | F _ {i}) \| q _ {L} (\cdot | F _ {i})) \right].\tag{29}
$$

The final objective is

$$
\begin{array}{c} \mathcal {L} _ {\text {Lite}} = (1 - \lambda_ {\text {KD}}) \mathcal {L} _ {\text {Lite}} ^ {(\sup)} + \lambda_ {\text {KD}} \mathcal {L} _ {\text {KD}}, \\ \theta_ {L} ^ {*} = \underset {\theta_ {L}} {\arg \min} \mathcal {L} _ {\text {Lite}}, \\ M _ {L} = (\theta_ {L} ^ {*}, \mathcal {G} _ {D}, d _ {L}). \end{array}\tag{30}
$$

This loss transfers flow-level decisions without changing the PTG-D topology.

The inherited PTG backbone represents each protocol field with a persistent schema node whose identity is shared across packets. PTT further uses this field-level alignment as a compression interface: learned node gates determine which protocol evidence is retained, while the protocol hierarchy determines how the retained evidence forms a valid reduced graph. This differs from compressing anonymous hidden channels or independently removing graph nodes, because every structural decision remains associated with a concrete protocol field and its original context. The same field identities are preserved across PTT-Full, PTT-Distilled, and PTT-Lite, which also provides a natural alignment for cross-stage parameter transfer.

## V. EVALUATION

## A. Experimental Setup

a) Datasets and Evaluation Protocol: We evaluate PTT on CSTNET-TLS1.3, which contains encrypted sessions across 26 domains, and CipherSpectrum, which contains 120,000 TLS 1.3 sessions across 41 domains and three cipher suites. All methods use identical flow-disjoint splits and SII-masked packet traces. The complete ETH layer, IP addresses, transport ports, and server names are removed before constructing each model’s input representation. PTT uses no composite TLS fingerprints such as JA3/JA4. Retained TLS fields remain individual nodes in their protocol hierarchy.

b) Compared Methods: We compare PTT-Full, PTT-Distilled, and PTT-Lite with image-like, byte/sequence, and graph classifiers, including RF [9], YaTC [8], TMWF [7], BAPM [2], Var-CNN [3], DF [4], Tik-Tok [5], AWF [16], Deep-Packet [6], ET-BERT [17], RBLJAN [15], GNN, and GAT. PTGAMoE [12], which uses dense PTG experts and supervised training, serves as the direct architectural baseline. All baselines are retrained under the same flow-disjoint splits and SII-masked inputs, rather than using their originally reported results.

c) Metrics and Inference Measurement: Accuracy and Macro-F1 measure classification performance. We additionally report parameter count (Params), effective GFLOPs (GFLOPs), CPU p50 latency (Lat.), and flow throughput (flow/s) to evaluate efficiency. Unless stated otherwise, GFLOPs count only the experts actually executed. Latency is measured over one macro-batch of $N _ { B } = 3 2$ flows, each retaining at most $P ~ = ~ 3 2$ packets. Packet parsing, protocol dissection, and input construction are excluded for all methods. For PTT, the timed forward pass includes gathering, sparse dispatch, graph execution, scattering, expert fusion, and classification. Flow throughput is computed as $\mathrm { F l o w s / s ~ = ~ }$ $\frac { N _ { B } } { \mathrm { L a t e n c y } / 1 0 0 0 }$ , where latency is measured in milliseconds per macro-batch. All models are benchmarked on the same CPU with the same macro-batch size, packet limit, and timing boundary.

d) Implementation Details: Code is available at https:// anonymous.4open.science/r/pruned traffic trees-D08C. Training uses a server with Intel i5-13490F CPU, 32 GB memory, and an NVIDIA RTX 4060 Ti 16 GB GPU. CPU inference uses a server with Intel i5-9500T and 8 GB memory. PTT-Full uses IP, TCP-core, TCP-option, TLS-record-header, and TLS-record-payload experts with $d _ { F } = 1 2 8$ . Unless otherwise stated, PTT-Distilled uses $K = 5$ and $d _ { D } = 3 2$ , and PTT-Lite uses $d _ { L } = 2 0$ . The Lite KD weights are 0.10 on CSTNET-TLS1.3 and 0.05 on CipherSpectrum.

![](images/2d2d14dd0cceaafa57441511056f590af74836d8370679d233eb5ce8b1842bf1.jpg)  
(a) CSTNET-TLS1.3.

![](images/b01f9ec184a7e1b57f00f7044cc83903596ae80722ab368dba15eaf4f682f722.jpg)  
(b) CipherSpectrum.

Fig. 3: Pareto frontiers of performance–latency trade-offs.  
![](images/9c3891e8ae3ed65f14eafd622c6212e3ac31e813d2b17b922fa70eaac3ca4338.jpg)  
Fig. 4: Compression effectiveness of PTT Family.

## B. Overall Performance and CPU Efficiency

Table I shows that PTT-Full achieves the highest Macro-F1 on both datasets. PTT-Lite retains 0.9325 and 0.9136 Macro-F1 with 0.186M and 0.481M parameters, exceeding GAT by 0.0663 and 0.0821, respectively. Compared with dense PTGAMoE, PTT-Full improves Macro-F1 by 0.0254 and 0.0707 while reducing macro-batch latency by 3.17× and 3.50×.

To jointly compare performance and latency, Fig. 3 plots the performance–latency trade-off leveraging Pareto frontiers. A model is non-dominated when no alternative has both higher Macro-F1 and lower latency. The PTT variants occupy the high-performance region on both datasets and provide distinct Full, Distilled, and Lite operating points.

## C. Compression Effectiveness

As shown in Fig. 4, the Full-to-Distilled transition, which jointly reduces PTG topology and representation width, accounts for most of the overall resource reduction. Table III further isolates the advantage of PTG-native structural compression under matched computation budgets. PTT-Lite keeps the distilled topology unchanged and further narrows the representation width. It uses only 19.72% and 38.70% of the Full-model parameters and 1.15% and 1.22% of its effective GFLOPs. The corresponding CPU speedups are 8.75× and 8.46×, indicating that structural compression provides the main reduction and width compression adds a lighter deployment point. This confirms that reducing protocol structures rather than only hidden dimensions is the main source of compression efficiency.

TABLE I: Overall comparison on CSTNET-TLS1.3 and CipherSpectrum.

<table><tr><td colspan="2">Dataset</td><td colspan="4">CSTNET-TLS1.3</td><td colspan="4">CipherSpectrum</td></tr><tr><td>Category</td><td>Method</td><td>AC</td><td>F1</td><td>Params (M)</td><td>Lat. (ms/batch)</td><td>AC</td><td>F1</td><td>Params (M)</td><td>Lat. (ms/batch)</td></tr><tr><td rowspan="2">Image-like</td><td>RF</td><td>0.3648</td><td>0.2996</td><td>0.924</td><td>4.73</td><td>0.6251</td><td>0.6318</td><td>0.947</td><td>4.41</td></tr><tr><td>YaTC</td><td>0.8756</td><td>0.8599</td><td>1.863</td><td>39.72</td><td>0.1162</td><td>0.1146</td><td>1.866</td><td>41.49</td></tr><tr><td rowspan="9">Byte/Sequence</td><td>TMWF</td><td>0.2953</td><td>0.2026</td><td>4.834</td><td>28.62</td><td>0.5289</td><td>0.5175</td><td>4.838</td><td>28.24</td></tr><tr><td>BAPM</td><td>0.4069</td><td>0.3505</td><td>0.238</td><td>1.48</td><td>0.5097</td><td>0.5028</td><td>0.269</td><td>1.49</td></tr><tr><td>Var-CNN</td><td>0.4963</td><td>0.4925</td><td>8.766</td><td>23.89</td><td>0.2455</td><td>0.2072</td><td>8.782</td><td>23.27</td></tr><tr><td>DF</td><td>0.3449</td><td>0.2555</td><td>3.679</td><td>5.25</td><td>0.5949</td><td>0.5913</td><td>3.687</td><td>5.20</td></tr><tr><td>Tik-Tok</td><td>0.2233</td><td>0.1378</td><td>3.679</td><td>5.20</td><td>0.7176</td><td>0.7135</td><td>3.687</td><td>5.25</td></tr><tr><td>AWF</td><td>0.2655</td><td>0.1908</td><td>0.048</td><td>0.59</td><td>0.3640</td><td>0.3389</td><td>0.069</td><td>0.59</td></tr><tr><td>Deep-Packet</td><td>0.0656</td><td>0.0305</td><td>10.108</td><td>2.67</td><td>0.0563</td><td>0.0026</td><td>10.109</td><td>2.40</td></tr><tr><td>ET-BERT</td><td>0.7761</td><td>0.7759</td><td>132.146</td><td>304.81</td><td>0.4059</td><td>0.3321</td><td>132.157</td><td>303.88</td></tr><tr><td>RBLJAN</td><td>0.8266</td><td>0.7859</td><td>0.357</td><td>60.44</td><td>0.5808</td><td>0.5427</td><td>0.499</td><td>74.88</td></tr><tr><td rowspan="3">Graph</td><td>GNN</td><td>0.8530</td><td>0.8230</td><td>0.026</td><td>1.51</td><td>0.7888</td><td>0.7880</td><td>0.029</td><td>1.37</td></tr><tr><td>GAT</td><td>0.8905</td><td>0.8662</td><td>0.141</td><td>1.61</td><td>0.8337</td><td>0.8315</td><td>0.144</td><td>1.46</td></tr><tr><td>PTGAMoE</td><td>0.9395</td><td>0.9265</td><td>0.962</td><td>1001.93</td><td>0.8720</td><td>0.8709</td><td>1.263</td><td>1150.57</td></tr><tr><td rowspan="3">PTT</td><td>PTT-Full</td><td>0.9646</td><td>0.9519</td><td>0.943</td><td>316.20</td><td>0.9415</td><td>0.9416</td><td>1.243</td><td>328.66</td></tr><tr><td>PTT-Distilled</td><td>0.9472</td><td>0.9380</td><td>0.218</td><td>41.79</td><td>0.9241</td><td>0.9238</td><td>0.513</td><td>48.31</td></tr><tr><td>PTT-Lite</td><td>0.9424</td><td>0.9325</td><td>0.186</td><td>36.12</td><td>0.9137</td><td>0.9136</td><td>0.481</td><td>38.85</td></tr></table>

## D. Effect of Presence-Aware Sparse Modeling

Table II separates the modeling effect of protocol-presence masking from the efficiency gain of actual sparse execution. Adding SSL alone (D1) provides limited gains over D0, whereas presence masking (D2) improves Macro-F1 and further combines with SSL (D3) to reach 0.9519 and 0.9416. D3 and D4 share the same checkpoints and predictions. D4 only enables sparse execution for absent protocol components. It reduces GFLOPs by 24.7% and 48.8%, latency by 27.9% and 48.4%, and increases throughput by 36.6% and 91.6%. Thus, presence masking improves protocol-aware modeling, while sparse execution turns protocol absence into computation savings without changing predictions.

## E. Effect of PTG-Native Structural Compression

This section examines four questions: (1) whether PTGnative compression is more effective than model-level compression; (2) whether learned field salience guides selection; (3) whether retained fields require their native hierarchy; and (4) how the field budget controls PTG-D size.

a) Model-Level versus PTG-Native Compression: We first compare PTT with three validation-tuned model-level baselines that retain the complete PTG. Narrow-CE (N-CE) reduces model width and trains the resulting full-PTG model with cross-entropy, while Narrow-KD (N-KD) additionally transfers PTT-Full logits. As a structured pruning baseline, $\ell _ { 2 } \cdot$ -based channel pruning (L2-Ch) ranks channels by the aggregated $\ell _ { 2 }$ norm of their associated weights and retains the highest-ranked channels before validation-tuned adaptation.

To ensure compute-matched comparison, we enumerate full-PTG widths $d \in \{ 4 , 8 , 1 2 , 1 6 , 2 0 , 2 4 , 2 8 , 3 2 \}$ and select the largest width whose validation-set effective GFLOPs do not exceed the corresponding PTT-Distilled or PTT-Lite budget. This yields d = 20 and d = 12, respectively, on both datasets. All baselines further tune the learning rate on $\{ 1 0 ^ { - 4 } , 2 \times$ $1 0 ^ { - 4 } , 5 \times 1 0 ^ { - 4 } \}$ , while N-KD and L2-Ch also tune their KD weights using validation data. The checkpoint with the highest validation Macro-F1 is then evaluated on the test set.

Table III shows that PTT consistently retains more classification performance than the strongest validation-tuned modellevel baseline. Its Macro-F1 gains are 0.0220 and 0.0324 at the Distilled budget, and increase to 0.0404 and 0.0743 at the Lite budget on CSTNET-TLS1.3 and CipherSpectrum, respectively. Although the full-PTG baselines use slightly fewer effective GFLOPs, their CPU latency is approximately 1.83× higher at the Distilled budget and 1.80× higher at the Lite budget. These results indicate that removing less informative protocol structure provides a better performance–efficiency trade-off than retaining the complete PTG and compressing model width or channels alone.

b) Field Guidance and Salience Stability: We next examine which real protocol fields should be retained before closure. Random (Rand.) samples candidate fields uniformly, Frequency (Freq.) ranks them by observation frequency in the training set, Taylor [37] uses first-order training-loss sensitivity, and NFS ranks fields according to the gates learned by PTT-Full. Because the NFS normalization is shared by all candidates within the same expert, it does not change their ordering. The resulting Top-K selection is determined by the learned gate salience. All methods use the same K = 5 and TopK+k closure.

As shown in Fig. 5, the learned gate salience produces the strongest compressed models under comparable graphcomputation budgets. We further examine the stability of the selected fields across three independent training runs. For experts with more than five candidate fields, the selected

TABLE II: Effect of SSL, protocol-presence masking, and actual expert skipping.

<table><tr><td>Dataset</td><td>ID</td><td>SSL</td><td>Mask</td><td>Sparse</td><td>F1</td><td>GFLOPs</td><td>Lat. (ms/batch)</td><td>Flows/s</td></tr><tr><td rowspan="5">CSTNET-TLS1.3</td><td>D0</td><td>✗</td><td>✗</td><td>✗</td><td>0.9296 (±0.0146)</td><td>9.241</td><td>436.04 [28.95]</td><td>73.54 [4.51]</td></tr><tr><td>D1</td><td>√</td><td>✗</td><td>✗</td><td>0.9301 (±0.0046)</td><td>9.241</td><td>436.94 [32.34]</td><td>73.57 [4.63]</td></tr><tr><td>D2</td><td>✗</td><td>√</td><td>✗</td><td>0.9415 (±0.0042)</td><td>9.241</td><td>436.87 [28.63]</td><td>73.51 [4.52]</td></tr><tr><td>D3</td><td>√</td><td>√</td><td>✗</td><td>0.9519 (±0.0111)</td><td>9.241</td><td>438.35 [31.08]</td><td>73.40 [4.80]</td></tr><tr><td>D4</td><td>√</td><td>√</td><td>√</td><td>0.9519 (±0.0111)</td><td>6.961</td><td>316.20 [18.53]</td><td>100.28 [6.00]</td></tr><tr><td rowspan="5">CipherSpectrum</td><td>D0</td><td>✗</td><td>✗</td><td>✗</td><td>0.9322 (±0.0042)</td><td>12.444</td><td>635.04 [24.82]</td><td>50.17 [2.13]</td></tr><tr><td>D1</td><td>√</td><td>✗</td><td>✗</td><td>0.9360 (±0.0074)</td><td>12.444</td><td>641.06 [26.53]</td><td>49.52 [2.04]</td></tr><tr><td>D2</td><td>✗</td><td>√</td><td>✗</td><td>0.9402 (±0.0036)</td><td>12.444</td><td>639.01 [25.61]</td><td>49.74 [2.12]</td></tr><tr><td>D3</td><td>√</td><td>√</td><td>✗</td><td>0.9416 (±0.0013)</td><td>12.444</td><td>637.52 [25.44]</td><td>49.96 [2.26]</td></tr><tr><td>D4</td><td>√</td><td>√</td><td>√</td><td>0.9416 (±0.0013)</td><td>6.371</td><td>328.66 [14.82]</td><td>95.73 [4.51]</td></tr></table>

Note: Latency and throughput are median [IQR] over 15 runs: three seeds and five repetitions per seed.

TABLE III: Validation-tuned model-level compression versus PTT under upper-bounded Distilled and Lite compute budgets.

<table><tr><td colspan="2"></td><td colspan="3">Distilled Budget</td><td colspan="3">Lite Budget</td></tr><tr><td>Dataset</td><td>Method</td><td>F1</td><td>GFLOPs</td><td>Lat.</td><td>F1</td><td>GFLOPs</td><td>Lat.</td></tr><tr><td rowspan="4">CSTNET TLS1.3</td><td>N-CE</td><td>0.9160</td><td>0.177</td><td>76.34</td><td>0.8261</td><td>0.075</td><td>65.38</td></tr><tr><td>N-KD</td><td>0.8867</td><td>0.177</td><td>75.86</td><td>0.8484</td><td>0.075</td><td>65.40</td></tr><tr><td>L2-Ch</td><td>0.9040</td><td>0.177</td><td>75.88</td><td>0.8921</td><td>0.075</td><td>64.85</td></tr><tr><td>PTT</td><td>0.9380</td><td>0.187</td><td>41.79</td><td>0.9325</td><td>0.080</td><td>36.12</td></tr><tr><td rowspan="4">Cipher Spectrum</td><td>N-CE</td><td>0.8914</td><td>0.173</td><td>88.25</td><td>0.7712</td><td>0.073</td><td>70.32</td></tr><tr><td>N-KD</td><td>0.8589</td><td>0.173</td><td>87.69</td><td>0.7749</td><td>0.073</td><td>70.34</td></tr><tr><td>L2-Ch</td><td>0.8850</td><td>0.173</td><td>87.72</td><td>0.8393</td><td>0.073</td><td>69.74</td></tr><tr><td>PTT</td><td>0.9238</td><td>0.182</td><td>48.31</td><td>0.9136</td><td>0.078</td><td>38.85</td></tr></table>

![](images/209eef05f7eef4c5e40ebc92b9a8438ba6b292907fd2e595ee2ca9705010f0d1.jpg)  
Fig. 5: Field-selector comparison under the same TopK+k closure and K = 5.

Top-5 sets achieve average pairwise Jaccard similarities of $0 . 4 2 8 6 \pm 0 . 1 4 3 1$ on CSTNET-TLS1.3 and $0 . 3 9 8 2 \pm 0 . 1 5 3 6$ on CipherSpectrum. The similar overlaps on both datasets indicate that the exact Top-K selections remain seed-sensitive rather than invariant. Nevertheless, repeatedly selected protocol fields form a more stable semantic core, while fields near the selection boundary may vary. Specifically, on CSTNET-TLS1.3, several fields, including IP length, TCP length, TLS cipher suite, and TLS extension type, are consistently retained across all seeds. The learned salience therefore provides a useful compression signal with a stable semantic core rather than a deterministic ranking of every protocol field.

c) Protocol Closure and Case Study: After fixing the selected fields, we examine whether their original hierarchical relations should also be retained. Selected Fields Only (SFO) keeps only the selected real fields. Selected + Ancestors (S+A) additionally retains the same ancestor nodes used by

TABLE IV: PTG-D retention schemes using the same NFSselected fields and $K \ = \ 5$ . Here, ‘A.N.’ denotes ancestor nodes, ‘H.E.’ denotes hierarchical edges, and ‘Comp.’ denotes path completeness, respectively.

<table><tr><td>Dataset</td><td>Scheme</td><td>A.N.</td><td>H.E.</td><td>Comp.</td><td>F1-D</td><td>F1-L</td></tr><tr><td rowspan="3">CSTNET TLS1.3</td><td>SFO</td><td>✗</td><td>✗</td><td>0.00</td><td>0.9010</td><td>0.8894</td></tr><tr><td>S+A</td><td>√</td><td>✗</td><td>0.00</td><td>0.8834</td><td>0.8636</td></tr><tr><td>TopK+k</td><td>√</td><td>√</td><td>1.00</td><td>0.9380</td><td>0.9325</td></tr><tr><td rowspan="3">Cipher Spectrum</td><td>SFO</td><td>✗</td><td>✗</td><td>0.00</td><td>0.8860</td><td>0.8663</td></tr><tr><td>S+A</td><td>√</td><td>✗</td><td>0.00</td><td>0.8679</td><td>0.8380</td></tr><tr><td>TopK+k</td><td>√</td><td>√</td><td>1.00</td><td>0.9238</td><td>0.9136</td></tr></table>

TopK+k, but removes their original parent–child relations. TopK+k retains both the required ancestors and their original hierarchical edges. Path completeness equals one only when every node and hierarchical edge on the original Full-PTG path of a selected field is retained.

Table IV shows that retaining additional ancestor nodes alone is insufficient. S+A keeps the same ancestor nodes as TopK+k but performs below even SFO when their original hierarchical relations are removed. In contrast, TopK+k achieves complete protocol paths and the highest Macro-F1 on both datasets. Together with Fig. 5, this result separates the two roles of PTG-native compression: learned field salience determines what protocol evidence is retained, while closure determines how that evidence remains connected to its native hierarchy.

Fig. 6 gives a concrete example using the TLS-Record-Header expert. Five real fields are selected by the learned salience, while closure restores three intermediate protocol nodes required by their original paths. For example, tls.recordheader.extension.type is retained together with tls, tls.recordheader, and tls.recordheader.extension, rather than becoming an isolated field. The resulting PTG-D reduces this expert from 19 to 8 PTG schema nodes, excluding the fixed sink, while preserving the protocol context of all selected fields.

d) Structural Reduction and Field Budget: We finally measure the actual graph reduction produced by the default K = 5 setting. PTG-D removes more than half of the graph structure on both datasets. CSTNET-TLS1.3 is reduced from 82 to 38 nodes and from 72 to 28 hierarchical edges, while CipherSpectrum is reduced from 88 to 38 nodes and from 78 to 28 edges. These correspond to node reductions of 53.66%– 56.82% and edge reductions of 61.11%–64.10%, while path completeness remains 1.00.

![](images/68ff95debf396787ee6bb68da085f15443dbf51858332e29ee2a7732da2a8f29.jpg)  
Fig. 6: PTG-D construction for the TLS-Record-Header expert.

![](images/630caa45b08c55a29712a7a6e95e862f69c01c3722eb61d583b63745ee8ce100.jpg)  
Fig. 7: Effect of the field budget K in TopK+k closure.

Compression is not uniform across experts: node retention ranges from 25.93% to 88.89% on CSTNET-TLS1.3 and from 25.93% to 85.71% on CipherSpectrum. PTT therefore fixes a semantic field budget rather than a graph-retention ratio. The final PTG-D size is determined by field availability and the protocol paths required by the selected fields.

Fig. 7 further varies this field budget. To emphasize the actual performance–computation trade-off, we report Macro-F1 and GFLOPs and omit parameter counts, which change only marginally with K.

On CSTNET-TLS1.3, the performance gain begins to saturate around K = 5: larger budgets increase graph computation substantially while providing smaller additional gains. Cipher-Spectrum benefits more consistently from additional fields and therefore admits higher-accuracy operating points at K = 10 or K = all. We use K = 5 as the common compact setting because it substantially reduces graph computation on both datasets while retaining strong classification performance.

## F. Effect of Cross-Stage Transfer

After obtaining PTG-D, we further investigate how knowledge is transferred from the structurally compressed teacher to the deployment-oriented Lite model. In the following experiments, the target PTG topology and model width are kept unchanged.

![](images/23e32169d0911e2e63830e2aa264f447ffec903b3088dbc258e261486a1bf390.jpg)

![](images/6328f0a6d370b45a7990012490b8c3d47542fe761cb283ba33caf3da32384943.jpg)  
(a) Effect of channel-projection initialization.  
(b) Effect of the logits-KD weight (λ<sub>KD</sub>) for PTT-Lite.

Fig. 8: Effect of Cross-Stage Transfer.  
TABLE V: Effect of the PTT-Lite hidden dimension $d _ { L } .$

<table><tr><td>Dataset</td><td> $d_L$ </td><td>F1</td><td>Params (M)</td><td>GFLOPs</td></tr><tr><td rowspan="3">CSTNET-TLS1.3</td><td>16</td><td>0.9275</td><td>0.178</td><td>0.054</td></tr><tr><td>20</td><td>0.9325</td><td>0.186</td><td>0.080</td></tr><tr><td>28</td><td>0.9318</td><td>0.206</td><td>0.146</td></tr><tr><td rowspan="3">CipherSpectrum</td><td>16</td><td>0.8883</td><td>0.473</td><td>0.053</td></tr><tr><td>20</td><td>0.9136</td><td>0.481</td><td>0.078</td></tr><tr><td>28</td><td>0.9346</td><td>0.501</td><td>0.143</td></tr></table>

a) Effect of Channel-Projection Initialization: Fig. 8(a) compares random initialization with structure-aligned projection. Projection improves Full-to-Distilled Macro-F1 by 0.0183 and 0.0032, and yields larger gains of 0.1085 and 0.0735 for Distilled-to-Lite. The larger Lite gains indicate that transferred channels mainly stabilize adaptation to an already fixed compact architecture.

b) Effect of Flow-Level Logits Distillation: Fig. 8(b) evaluates whether flow-level teacher predictions provide additional guidance after width reduction. On CSTNET-TLS1.3, $\lambda _ { \mathrm { K D } } ~ = ~ 0 . 1 0$ raises Macro-F1 from 0.9129 to 0.9325. CipherSpectrum benefits only marginally at 0.05 and degrades under larger teacher weights. Logits distillation is therefore complementary and dataset-dependent rather than the main source of structural-compression gains.

c) Effect of Width Selection: Table V varies $d _ { L }$ within the fixed PTG-D topology. On CSTNET-TLS1.3, increasing $d _ { L }$ from 16 to 20 improves Macro-F1, while $d _ { L } = 2 8$ adds computation without further gain. CipherSpectrum needs more capacity: $d _ { L } \ = \ 1 6$ degrades clearly, and $d _ { L } \ = \ 2 8$ reaches 0.9346 at 0.143 GFLOPs. We use $d _ { L } \ = \ 2 0$ as a common balanced point, while $d _ { L } = 2 8$ remains an accuracy-oriented option for CipherSpectrum.

## VI. CONCLUSION

We present Pruned Traffic Trees (PTT), a protocolstructured ETC model family that makes native protocol structures directly compressible. PTT determines what protocol evidence to retain through learned field salience and how to preserve its structural context through TopK+k closure, constructing compact PTG-Ds without breaking native protocol paths. Together with sparse execution and cross-stage adaptation, PTT provides practical Full, Distilled, and Lite operating points. Experiments under flow-disjoint and SIImasked settings demonstrate strong Macro-F1 with substantially reduced graph computation and CPU latency. Future work will investigate end-to-end parsing overhead, optimize graph execution, and extend PTT to broader protocols.

## REFERENCES

[1] E. Papadogiannaki and S. Ioannidis, “A survey on encrypted network traffic analysis applications, techniques, and countermeasures,” ACM Computing Surveys (CSUR), vol. 54, no. 6, pp. 1–35, 2021.

[2] Z. Guan, G. Xiong, G. Gou, Z. Li, M. Cui, and C. Liu, “Bapm: block attention profiling model for multi-tab website fingerprinting attacks on tor,” in Proceedings of the 37th Annual Computer Security Applications Conference, 2021, pp. 248–259.

[3] S. Bhat, D. Lu, A. Kwon, and S. Devadas, “Var-cnn: A data-efficient website fingerprinting attack based on deep learning,” arXiv preprint arXiv:1802.10215, 2018.

[4] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proceedings of the 2018 ACM SIGSAC conference on computer and communications security, 2018, pp. 1928–1943.

[5] M. S. Rahman, P. Sirinam, N. Mathews, K. G. Gangadhara, and M. Wright, “Tik-tok: The utility of packet timing in website fingerprinting attacks,” arXiv preprint arXiv:1902.06421, 2019.

[6] M. Lotfollahi, M. Jafari Siavoshani, R. Shirali Hossein Zade, and M. Saberian, “Deep packet: A novel approach for encrypted traffic classification using deep learning,” Soft Computing, vol. 24, no. 3, pp. 1999–2012, 2020.

[7] Z. Jin, T. Lu, S. Luo, and J. Shang, “Transformer-based model for multitab website fingerprinting attack,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1050–1064.

[8] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 5420–5427.

[9] M. Shen, K. Ji, Z. Gao, Q. Li, L. Zhu, and K. Xu, “Subverting website fingerprinting defenses with robust traffic representation,” in 32nd USENIX Security Symposium (USENIX Security 23), 2023, pp. 607–624.

[10] Y. Zhu, J. Tao, H. Wang, L. Yu, Y. Luo, T. Qi, Z. Wang, and Y. Xu, “Dgnn: Accurate darknet application classification adopting attention graph neural network,” IEEE Transactions on Network and Service Management, 2023.

[11] Y. Tian, S. Pei, X. Zhang, C. Zhang, and N. V. Chawla, “Knowledge distillation on graphs: A survey,” ACM Computing Surveys, vol. 57, no. 8, pp. 1–16, 2025.

[12] Y. Luo, J. Tao, L. Yu, and G. Cheng, “Treat traffic like trees: A semanticpreserving hierarchical graph-based expert framework for encrypted traffic analysis,” arXiv preprint arXiv:2606.04517, 2026.

[13] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “Sok: Decoding the enigma of encrypted network traffic classifiers,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE, 2025, pp. 1825– 1843.

[14] Y. Zhao, G. Dettori, M. Boffa, L. Vassio, and M. Mellia, “The sweet danger of sugar: Debunking representation learning for encrypted traffic classification,” in Proceedings ofthe ACM SIGCOMM 2025 Conference, 2025, pp. 296–310.

[15] X. Xiao, S. Wang, G. Hu, Q. Li, K. Mao, X. Luo, B. Zhang, and S. Xia, “Rbljan: Robust byte-label joint attention network for network traffic classification,” IEEE Transactions on Dependable and Secure Computing, 2024.

[16] V. Rimmer, D. Preuveneers, M. Juarez, T. Van Goethem, and W. Joosen, “Automated website fingerprinting through deep learning,” arXiv preprint arXiv:1708.06376, 2017.

[17] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.

[18] X. Qiu, G. Cheng, W. Zhu, D. Niu, and N. Fu, “Dual-channel interactive graph transformer for traffic classification with message-aware flow representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 39, no. 1, 2025, pp. 685–693.

[19] K. Feng, C. Li, Y. Yuan, and G. Wang, “Freekd: Free-direction knowledge distillation for graph neural networks,” in Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2022, pp. 357–366.

[20] Z. Guo, C. Zhang, Y. Fan, Y. Tian, C. Zhang, and N. V. Chawla, “Boosting graph neural networks via adaptive knowledge distillation,” in Proceedings of the AAAI conference on artificial intelligence, vol. 37, no. 6, 2023, pp. 7793–7801.

[21] C. Huo, D. Jin, Y. Li, D. He, Y.-B. Yang, and L. Wu, “T2-gnn: Graph neural networks for graphs with incomplete features and structure via teacher-student distillation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 4339–4346.

[22] L. Yu, S. Pei, L. Ding, J. Zhou, L. Li, C. Zhang, and X. Zhang, “Sail: Self-augmented graph contrastive learning,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 36, no. 8, 2022, pp. 8927– 8935.

[23] H. He, J. Wang, Z. Zhang, and F. Wu, “Compressing deep graph neural networks via adversarial knowledge distillation,” in Proceedings of the 28th ACM SIGKDD conference on knowledge discovery and data mining, 2022, pp. 534–544.

[24] W. Zhang, X. Miao, Y. Shao, J. Jiang, L. Chen, O. Ruas, and B. Cui, “Reliable data distillation on graph convolutional network,” in Proceedings of the 2020 ACM SIGMOD international conference on management of data, 2020, pp. 1399–1414.

[25] J. Guo, D. Chen, and C. Wang, “Alignahead: Online cross-layer knowledge extraction on graph neural networks,” in 2022 International Joint Conference on Neural Networks (IJCNN). IEEE, 2022, pp. 1–8.

[26] C. Wang, S. Zhou, K. Yu, D. Chen, B. Li, Y. Feng, and C. Chen, “Collaborative knowledge distillation for heterogeneous information network embedding,” in Proceedings of the ACM web conference 2022, 2022, pp. 1631–1639.

[27] W. Zheng, E. W. Huang, N. Rao, S. Katariya, Z. Wang, and K. Subbian, “Cold brew: Distilling graph node representations with incomplete or missing neighborhoods,” in International Conference on Learning Representations, 2022.

[28] Z. Zhang, Z. Luan, Q. Li, Z. Qi, K. Li, Y. Jiang, and Z. Yuan, “Sentinelx: A lightweight malicious traffic detection system based on programmable switches,” in IEEE INFOCOM 2025-IEEE Conference on Computer Communications. IEEE, 2025, pp. 1–10.

[29] C. Fu, Q. Li, E. Bertino, and K. Xu, “Training with only 1.0‰ samples: Malicious traffic detection via cross-modality feature fusion,” in Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, 2025, pp. 3930–3944.

[30] J. Lu, K. Yu, Y. Huang, Z. Wei, J. Yin, and X. Liu, “Seadgat: A heterogeneous graph attention network with cross distillation for encrypted traffic classification,” IEEE Internet of Things Journal, 2026.

[31] X. Lian, Y. Zheng, Y. Liu, F. Zhou, C. Peng, and X. Gao, “Contextual masking distillation for network traffic anomaly detection,” IEEE Transactions on Information Forensics and Security, 2026.

[32] C. Riquelme, J. Puigcerver, B. Mustafa, M. Neumann, R. Jenatton, A. Susano Pinto, D. Keysers, and N. Houlsby, “Scaling vision with sparse mixture of experts,” Advances in Neural Information Processing Systems, vol. 34, pp. 8583–8595, 2021.

[33] W. Cai, J. Jiang, F. Wang, J. Tang, S. Kim, and J. Huang, “A survey on mixture of experts in large language models,” IEEE Transactions on Knowledge and Data Engineering, 2025.

[34] J. Zhou, C. Sun, M. Shen, S. Yu, and Q. Xuan, “Traffic-moe: A sparse foundation model for network traffic analysis,” arXiv preprint arXiv:2601.00357, 2026.

[35] Q. He, X. Fu, and L. Zhang, “Trafficmoe: Heterogeneity-aware mixture of experts for encrypted traffic classification,” arXiv preprint arXiv:2603.29520, 2026.

[36] J. Qin, X. Han, Y. Li, D. Han, W. Qiao, X. Yang, Z. Cui, B. Jiang, and Z. Lu, “Trafficmoe: Adaptive multi-perspective feature fusion for enhancing malicious traffic general detection capability,” in ICASSP 2026-2026 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2026, pp. 14 242–14 246.

[37] P. Molchanov, S. Tyree, T. Karras, T. Aila, and J. Kautz, “Pruning convolutional neural networks for resource efficient inference,” in International conference on learning representations, 2017.