# IMPROVING THE RELIABILITY OF ANOMALY DETECTION FOR ENCRYPTED OPC UA TRAFFIC OVER PRIVATE 5G

A PREPRINT

Song Son Ha Electrical Measurement Engineering Helmut-Schmidt-University Hamburg, Germany song.ha@hsu-hh.de

Henry Beuster Electrical Measurement Engineering Helmut-Schmidt-University Hamburg, Germany henry.beuster@hsu-hh.de

Dominik Merli Institute for Innovative Safety and Security Technical University of Applied Sciences Augsburg Augsburg, Germany dominik.merli@tha.de

Florian Foerster Institute for Innovative Safety and Security Technical University of Applied Sciences Augsburg Augsburg, Germany florian.foerster@tha.de

Tim Kittel ipoque GmbH A Rohde & Schwarz company Leipzig, Germany tim.kittel@rohde-schwarz.com

Gerd Scholl Electrical Measurement Engineering Helmut-Schmidt-University Hamburg, Germany gerd.scholl@hsu-hh.de

September 24, 2026

## ABSTRACT

Open Platform Communications Unified Architecture (OPC UA) is increasingly deployed over private 5G networks in industrial environments, where end-to-end encryption prevents payload inspection by network-based intrusion detection systems (IDSs). Although payload-agnostic statistical features extracted from encrypted traffic enable traffic-based anomaly detection, benign connectivity variations may alter observable user-plane (UP) behavior and increase the false-positive rate (FPR). This paper investigates this reliability problem and proposes a control-plane (CP)-aware decision adaptation for four frozen IDS models. CP indicators at the user equipment (UE) level are used to construct a temporal CP context in which a CP-specific threshold selected on adaptation validation data is applied, while the original threshold remains active outside the context. The traffic features, attack scores, preprocessing procedure, and trained model parameters remain unchanged.

Evaluation on a real industrial private 5G testbed shows that benign connectivity variations increase the FPR for all four evaluated models and that false positives are concentrated within periods temporally associated with CP activity. The proposed CP-aware decision adaptation reduces both global FPR and FPR within the CP context while introducing a configurable trade-off between FPR reduction and retained recall over the complete attack campaign. These findings demonstrate that CP context can improve the operational reliability of encrypted-traffic intrusion detection without retraining the underlying models.

Keywords: OPC UA, Encrypted Traffic Analysis, Anomaly Detection, Private 5G, Control-Plane Context

## 1 Introduction

Open Platform Communications Unified Architecture (OPC UA) is widely used in industrial automation because of its interoperability, extensibility, and integrated security mechanisms [1]. Private 5G networks provide dedicated wireless connectivity and quality-of-service control for heterogeneous industrial devices and applications. Their combination supports flexible wireless industrial communication, but end-to-end OPC UA encryption limits network-side security monitoring. When using the SignAndEncrypt security mode, application payloads and service semantics are not accessible at the monitoring point. Intrusion detection must therefore rely on remaining payload-agnostic traffic characteristics such as packet sizes, timing, directionality, flow dynamics, and observable protocol framing.

Traffic-based intrusion detection system (IDS) models are commonly calibrated and evaluated under relatively stable connectivity conditions. Benign user equipment (UE) reconnections, Protocol Data Unit (PDU) session changes, and temporary communication interruptions may alter observable user-plane (UP) traffic without indicating malicious activity. The resulting changes in traffic intensity, timing, and session behavior can resemble application anomalies and increase the false-positive rate (FPR).

Previous work [2] experimentally demonstrated that benign private 5G connectivity variations increase the FPR of IDS models for encrypted OPC UA traffic. Elevated attack scores also occurred frequently during or shortly after UE-level control-plane (CP) activity. That study used CP indicators only to interpret IDS outputs and did not introduce a mechanism for adapting IDS decisions. It also did not evaluate the effect of such adaptation when attacks and benign connectivity variations occur within the same capture.

This paper extends the preceding study from temporal interpretation to decision adaptation. Lightweight UE-level CP indicators are used to construct a temporal CP context associated with connectivity activity. The adaptation operates only at the decision stage of the frozen IDS models. CP-specific thresholds are selected using benign variation adaptation validation data to reduce FPR and mixed variation–attack adaptation validation data to constrain the reduction in recall over the complete attack campaign.

The main contributions of this work are as follows:

• A systematic quantification of false-positive concentration within and outside the temporal CP context across four frozen IDS models under controlled benign connectivity variations.

• A CP-aware decision adaptation that applies a CP-specific threshold only within the temporal CP context while preserving the underlying traffic-based IDS.

• A validation procedure that selects CP-specific operating points under explicit constraints on recall over the attack campaign, followed by a separate test evaluation using benign variation and mixed variation–attack captures.

The remainder of this paper is organized as follows. Section 2 reviews related work. Section 3 presents the proposed methodology. Section 4 describes the experimental implementation and dataset construction. Section 5 reports the evaluation results. Section 6 concludes the paper and outlines directions for future work.

## 2 Related Work

Research related to this work covers encrypted traffic analysis, intrusion detection for encrypted OPC UA communica tion, analysis of 5G control-plane behavior, and the use of operational context in anomaly detection.

Encrypted traffic analysis commonly relies on statistical characteristics observable without application-payload access, including packet sizes, timing, directionality, and flow statistics [3, 4]. Such representations can change across deployment conditions: Malekghaini et al. [5] report degradation of encrypted-traffic classifiers under real-world data drift, while Qing et al. [6] study robust classification under dynamic network conditions. Although classification-focused, these studies show that traffic-derived model behavior need not remain stable after deployment.

For OPC UA, Honda et al. [1, 7] address the loss of direct visibility caused by encryption through an intermediary monitoring architecture that decrypts the communication. Neu et al. [8] investigate attacks by untrusted OPC UA clients, including encrypted denial-of-service traffic, and corresponding detection approaches. In the broader industrial domain, Wu et al. [9] propose anomaly detection for encrypted ICS traffic. Statistical features extracted from encrypted OPC UA traffic have also been shown to support the detection of protocol-compliant attacks over industrial private 5G [10].

These studies establish the feasibility of security monitoring despite encrypted industrial traffic, but do not examine how benign private 5G connectivity procedures affect the operating point of a frozen detector.

Several studies analyze anomaly detection in the 5G control plane using Non-Access Stratum (NAS), NG Application Protocol (NGAP), and core-network signaling sequences [11, 12, 13]. Their objective is to identify abnormal signaling behavior, mobility anomalies, or irregular session procedures within the 5G infrastructure. Here, CP indicators are neither classified nor included in the traffic-based IDS input; they provide temporal context for encrypted user-plane traffic. MobiFlow [14] combines UE state, control-plane message sequences, user-plane traffic, and connection-related statistics for security analysis. Abdelrahman and Gelenbe use network KPIs and data-plane traffic measurements to detect control-plane anomalies in mobile networks [15]. Neither approach uses benign UE-level CP activity to gate the decision threshold of an otherwise frozen user-plane IDS.

Context-aware anomaly detection uses auxiliary information to distinguish abnormal observations from legitimate operating changes. Existing approaches incorporate context into feature representations, model structures, or online adaptation [16, 17, 18]. Threshold selection is an important component of network anomaly detection, with supervised and unsupervised strategies providing different approaches to deriving decision thresholds [19]. At the decision stage, Ali et al. [20] adapt anomaly thresholds under time-varying network and host inputs, Gamallo-Fernández et al. [21] define separate thresholds for different execution conditions, and Zelasko [<sup>˙</sup> 22] formulates validation-based operating points that may be indexed by operational context in a network IDS. These works establish adaptive and context-dependent thresholding as general mechanisms, but do not use transient UE-level 5G CP activity to activate a secondary threshold for an otherwise unchanged encrypted application-traffic detector.

The preceding study [2] further showed that benign 5G connectivity variations increase the FPR of encrypted OPC UA traffic-based IDS models and that elevated attack scores are temporally associated with CP activity, but used this information only for interpretation. The present study extends this analysis by using UE-level CP activity as temporal context for decision adaptation, selecting CP-specific operating points under an explicit campaign recall constraint, and evaluating them on mixed variation–attack captures.

## 3 Proposed Methodology

This section describes the proposed CP-aware decision adaptation for encrypted OPC UA traffic over private 5G.

## 3.1 Overview of the Proposed CP-Aware Decision Adaptation

The proposed adaptation combines traffic-based anomaly detection with CP context at the decision stage. Encrypted UP traffic is summarized over fixed time windows (TWs) and processed by a frozen IDS model to obtain an attack score for each TW. In parallel, UE-level CP indicators are aligned with the same TWs to construct a temporal CP context representing periods of connectivity activity. A CP-specific threshold selected during adaptation validation is applied within the CP context, while the original threshold remains active outside it. The CP information is therefore used only at the decision stage and does not affect the attack scores produced by the frozen IDS model.

## 3.2 Threat Model

This work considers a secured private 5G environment with encrypted and authenticated OPC UA communication [23]. All sessions use the SignAndEncrypt security mode, preventing the network-based IDS from inspecting plaintext application payloads and service semantics. An adversary may control or compromise an authorized OPC UA endpoint and generate syntactically valid malicious behavior within encrypted sessions without breaking the cryptographic mechanisms. The resulting attacks are therefore reflected in observable traffic dynamics rather than malformed packets or explicit protocol violations. The considered 5G connectivity variations are benign and are not initiated by the adversary. The UE-level CP telemetry used for the adaptation is assumed to be trusted and correctly time-aligned with the UP observations. Adversarial manipulation of CP telemetry or intentional triggering of CP activity is outside the present threat model.

## 3.3 Traffic Representation and Frozen IDS Models

Each capture is divided into consecutive, non-overlapping 5 s TWs. For every TW, bidirectional OPC UA communication is represented using traffic volume and direction, temporal and flow dynamics, and observable OPC UA framing and lifecycle activity [10]. Flow-level measurements are aggregated into one feature vector per TW.

Table 1: UE-level CP indicators extracted from NAS and NGAP traces

<table><tr><td>CP Indicator</td><td>Description</td></tr><tr><td>Registration Event</td><td>Binary flag indicating the occurrence of a 5G registration or deregistration procedure.</td></tr><tr><td>CM State Transition</td><td>Binary flag indicating signaling associated with transitions between CM-IDLE and CM-CONNECTED, derived from NAS and NGAP.</td></tr><tr><td>PDU Session State Change</td><td>Binary flag indicating PDU session establishment or release activity.</td></tr><tr><td>PDU Resource Reconfiguration</td><td>Binary flag indicating an NGAP PDU session resource setup, modify, or release procedure.</td></tr><tr><td>CP Signaling Count</td><td>Aggregate number of CP signaling frames containing NAS-5GS or NGAP information within the TW.</td></tr></table>

The evaluation considers Logistic Regression (LogReg), Random Forest (RF), Support Vector Machine with a radial basis function kernel (SVM), and Extreme Gradient Boosting (XGBoost). Model development and baseline evaluation are described in [10]. The traffic representation, preprocessing procedure, model parameters, score functions, and original decision thresholds $\tau _ { m }$ remain fixed throughout the evaluation. The benign variation and mixed variation–attack datasets are not used to retrain the models or recalibrate their original thresholds. CP indicators are processed separatel and affect only the decision adaptation.

## 3.4 CP Context Indicators

Benign connectivity procedures may temporarily alter UP communication and increase the FPR of traffic-based IDS models. The proposed method uses UE-level CP signaling to identify the time intervals associated with these procedures. The CP indicators are derived from NAS and NGAP messages collected by the core network operations and monitoring framework. Only signaling associated with the UE subjected to the connectivity variation is processed. In captures containing both a connectivity variation and an attack, the CP indicators are extracted from the UE subjected to the variation, which is different from the attacked UE.

Table 1 summarizes the selected indicators. The procedure-specific indicators represent registration activity, Connection Management (CM) state transitions, Protocol Data Unit (PDU) session activity, and access-side PDU resource procedures. The aggregate CP signaling count provides a procedure-agnostic indication of UE-level CP activity. It therefore preserves CP activity that is not mapped to one of the selected procedure-specific indicators and also provides a consistency check for their extraction.

For each TW t, the CP indicators form a context vector $\mathbf { c } _ { t } .$ . A TW is marked as CP-active when at least one component of $\mathbf { c } _ { t }$ is nonzero. CP-active TWs that are temporally close are merged into CP activity clusters using a maximum internal gap. The temporal CP context is then obtained by extending the resulting clusters with configurable pre- and post-padding. The gap and padding parameters are selected exclusively on the benign variation adaptation validation captures and are fixed before test evaluation.

## 3.5 CP-Aware Decision Adaptation

The proposed adaptation changes only the decision threshold. For IDS model m and TW t, let $s _ { m , t } \in \mathbb { R }$ denote the attack score and let $\tau _ { m }$ denote the original threshold of the frozen model. Thresholds are handled separately because the ranges of the attack scores differ across models. The original decision is

$$
d _ {m, t} = \left\{ \begin{array}{l l} 1, & s _ {m, t} \geq \tau_ {m}, \\ 0, & s _ {m, t} <   \tau_ {m}, \end{array} \right.\tag{1}
$$

where $d _ { m , t } = 1$ denotes an attack prediction. The CP indicators are not included in the model input and do not affect $s _ { m , t } .$

## 3.5.1 Decision Rule with CP Context

Let $q _ { t } \in \{ 0 , 1 \}$ indicate whether TW t belongs to the temporal CP context defined in Section 3.4. A CP-specific threshold $\tau _ { m , \mathrm { C P } }$ is applied when $q _ { t } = 1$ , while the original threshold $\tau _ { m }$ remains active when $q _ { t } = 0$ . The threshold used at TW t is

$$
\tau_ {m, t} ^ {\mathrm{CP}} = (1 - q _ {t}) \tau_ {m} + q _ {t} \tau_ {m, \mathrm{CP}}.\tag{2}
$$

The adapted decision is

$$
\tilde {d} _ {m, t} = \left\{ \begin{array}{l l} 1, & s _ {m, t} \geq \tau_ {m, t} ^ {\mathrm{CP}}, \\ 0, & s _ {m, t} <   \tau_ {m, t} ^ {\mathrm{CP}}. \end{array} \right.\tag{3}
$$

Only thresholds satisfying $\tau _ { m , \mathrm { C P } } \geq \tau _ { m }$ are evaluated. The adaptation can suppress attack predictions within the CP context but cannot introduce new ones. Decisions outside the context remain unchanged.

The CP context is not interpreted as evidence that a TW is benign. It identifies intervals in which benign connectivity procedures may alter UP traffic and increase false positives. Genuine attacks may also occur within these intervals. The CP-specific threshold is therefore selected under a constraint on recall over the complete attack campaign.

## 3.5.2 Construction of Tested Thresholds

For model $m ,$ , let λ denote one threshold value to be tested within the CP context. During the evaluation of $\lambda ,$ the decision rule in (2) is applied by setting $\tau _ { m , \mathrm { C P } } = \lambda$ . The possible values of λ are derived from the attack scores $s _ { m , t }$ of TWs within the CP context whose scores satisfy $s _ { m , t } \geq \tau _ { m }$ under the original decision rule. On the benign variation adaptation validation set, every TW is benign. Therefore, each selected score $s _ { m , t }$ directly corresponds to a false-positive decision made by the original threshold.

On the mixed variation–attack adaptation validation set, the selected scores $s _ { m , i }$ belong to evaluated TWs within the attack campaign that satisfy $s _ { m , t } \geq \tau _ { m }$ and therefore correspond to correct attack predictions. Increasing the CP-specific threshold may suppress the false positives represented by the first group, but may also remove correct attack predictions represented by the second group.

Let $S _ { m }$ denote the set of attack scores $s _ { m , t }$ obtained from these two groups of TWs. Repeated score values are considered only once. For each $s _ { m , t } \in S _ { m }$ , the procedure tests the smallest representable threshold $s _ { m , t } ^ { + } > s _ { m , t }$ <sub>t</sub>. When ${ \lambda = s _ { m , t } ^ { + } }$ is applied within the CP context, TWs with score $s _ { m , t }$ are classified as benign because $s _ { m , t } < \lambda$

$$
\mathcal {C} _ {m} = \left\{\tau_ {m} \right\} \cup \left\{s _ {m, t} ^ {+} \mid s _ {m, t} \in \mathcal {S} _ {m} \right\}.\tag{4}
$$

Including $\tau _ { m }$ allows the original decision rule to remain a possible operating point. Every threshold $\lambda \in \mathcal { C } _ { m }$ satisfies $\lambda \geq \tau _ { m } ,$ so the adaptation can suppress attack predictions within the CP context but cannot introduce additional ones.

## 3.5.3 Selection of Operating Points

For each threshold $\lambda \in { \mathcal { C } } _ { m } .$ , the global FPR is measured on the benign variation adaptation validation set, while the corresponding reduction in campaign recall is measured on the mixed variation–attack adaptation validation set. Each λ is evaluated as a possible value of $\tau _ { m , \mathrm { C P } }$ . For a given tolerance $\delta _ { \mathrm { v a l } }$ <sub>l</sub>, the selected value is denoted by $\tau _ { m , \mathrm { C P } } ^ { ( \delta _ { \mathrm { v a l } } ) }$

Each mixed variation–attack capture contains repeated attack bursts separated by inter-burst intervals. The complete attack campaign extends from the first to the final attack-burst TW, including the intervening inter-burst TWs.

Let $R _ { m , \mathrm { c a m p } } ^ { ( \tau _ { m } ) }$ denote recall over these TWs when the original threshold is used both within and outside the CP context. Let $R _ { m , \mathrm { { c a m p } } } ^ { ( \lambda ) }$ denote the corresponding recall when λ is applied within the CP context and $\tau _ { m }$ remains active outside it. The campaign recall reduction on the adaptation validation set, expressed in percentage points (pp), is

$$
\Delta R _ {m, \text {camp}} ^ {(\lambda)} = 1 0 0 \left(R _ {m, \text {camp}} ^ {(\tau_ {m})} - R _ {m, \text {camp}} ^ {(\lambda)}\right).\tag{5}
$$

The evaluated tolerances are

$$
\mathcal {D} = \{0, 0. 5, 1, 2, 5 \} \mathrm{pp},\tag{6}
$$

For each tolerance $\delta _ { \mathrm { v a l } } \in \mathcal { D }$ , the selected CP-specific threshold is

$$
\begin{array}{c} \tau_ {m, \mathrm{CP}} ^ {(\delta_ {\mathrm{val}})} = \underset {\lambda \in \mathcal {C} _ {m}} {\arg \min} \operatorname{FPR} _ {m, \mathrm{var}} ^ {(\lambda)} \\ \text {subject to} \quad \Delta R _ {m, \mathrm{camp}} ^ {(\lambda)} \leq \delta_ {\mathrm{val}}. \end{array}\tag{7}
$$

Here, $\mathrm { F P R } _ { m , \mathrm { v a r } } ^ { ( \lambda ) }$ denotes the global FPR measured on the benign variation adaptation validation set when λ is applied within the CP context. From $\mathcal { C } _ { m } .$ the procedure selects the threshold that produces the lowest validation FPR while satisfying the permitted campaign recall reduction. As an additional validation safeguard, candidate thresholds that reduce attack-burst recall by more than the same tolerance $\delta _ { \mathrm { v a l } }$ are excluded.

A tolerance of 0 pp requires campaign recall to remain unchanged on the mixed variation–attack adaptation validation set, while the attack-burst safeguard prevents a recall reduction during attack bursts. This condition does not require $\tau _ { m , \mathrm { C P } } ^ { ( \delta _ { \mathrm { v a l } } ) } = \tau _ { m } ,$ because a higher threshold may suppress false positives without violating the validation constraints. Larger tolerances permit greater recall reductions and may therefore provide a larger FPR reduction.

If several thresholds produce the same minimum FPR, preference is given to the threshold with the smaller maximum reduction across campaign recall and attack-burst recall. Remaining ties are resolved using the smaller inter-burst recall reduction and then the smaller threshold increase.

## 3.5.4 Test Evaluation

The complete set of operating points selected for the five validation tolerances is fixed before test evaluation. Global FPR and FPR within the CP context are measured on the benign variation test captures. Campaign recall is measured separately on the mixed variation–attack test captures. FPR reduction is reported relative to the corresponding FPR under the original decision rule, while campaign recall reduction is reported in pp. The FPR outside the CP context remains unchanged because the original threshold $\tau _ { m }$ is retained in these TWs. No test capture is used to select the CP-context parameters, construct $\mathcal { C } _ { m }$ , or select an operating point. The validation constraints are applied only during adaptation validation. Campaign recall reduction on the mixed variation–attack test captures may exceed the corresponding tolerance and does not trigger threshold reselection.

## 4 Implementation

## 4.1 Experimental Environment

The experiments are conducted on the industrial private 5G testbed described in [24]. The OPC UA application operates under the encrypted configuration described in [10]. Only the components relevant to the present data collection are summarized here. The platform provides a standalone network compliant with 3GPP Release 16, mirrored UP traffic, and UE-level CP traces. A warehouse automation process is emulated using Factory I/O [25]. Revolution Pi controllers execute the programmable logic controller functions and host OPC UA endpoints. Humanmachine interface, supervisory control and data acquisition, engineering, diagnostic, and remote controller systems generate the industrial communication workloads. All OPC UA sessions use the SignAndEncrypt security mode with the Aes128-Sha256-RsaOaep security policy. Mirrored UP traffic is transferred to the IDS backend, where the R&S<sup>®</sup>PACE 2 library extracts observable traffic and OPC UA framing information without decrypting service payloads. The resulting observations are aggregated into TWs. CP traces are collected separately for the relevant UE and aligned with the UP observations during dataset construction. Fig. 1 shows the physical components of the testbed.

![](images/b61896fa96a779a443b7e7cd9ab429f388c74c7aa390783900ba7f541ec017fb.jpg)  
Figure 1: Experimental testbed: 1) 5G radio units; 2) SIMCom SIM8202G-M2 modules; 3) Revolution Pi modules; 4) Factory I/O system; 5) Raspberry Pi 5 modules; 6) Intel NUC; 7) attack workstation; 8) Siemens Scalance M800 router; 9) IDS backend; and 10) testbed orchestrator. The 5G core network, central and distributed units, telemetry services, and remote engineering systems are not shown.

## 4.2 Attack Scenarios

The attack implementations extend the OPC UA exploitation framework provided by Claroty [26] to operate through authorized OPC UA clients under the SignAndEncrypt security mode. The evaluated families are Browse Address Space, Publish Request Flooding, Persistent Secure Channel Exhaustion, and Translate Browse Path, targeting addressspace traversal, subscription processing, SecureChannel and session resources, and browse-path resolution, respectively. Each family is executed at four configuration levels using repeated attack bursts separated by inter-burst intervals. The parameter settings and configuration progression are described in [10].

## 4.3 Controlled Connectivity Variation Scenarios

The evaluation considers four controlled benign connectivity variations. Each variation is triggered on a selected UE and invokes a specific private 5G connectivity procedure without introducing malicious application behavior. The scenarios are designed to produce representative changes in CP signaling and UP communication that may affect the decisions of the frozen traffic-based IDS models. Table 2 summarizes the implemented procedures, their expected effects, and representative industrial contexts.

## 4.4 Dataset Construction and Partitioning

The dataset comprises 522 captures with a nominal duration of 10 min each, corresponding to a nominal total of 87 h of traffic. Actual capture durations vary slightly depending on the completion of the experimental procedure. All captures are partitioned before extraction of the non-overlapping 5 s TWs, and no capture appears in more than one subset. Table 3 summarizes the capture-level partitioning.

Table 2: Overview of controlled benign connectivity variation scenarios

<table><tr><td>Scenario</td><td>Description</td><td>Expected Effects</td><td>Example Industrial Context</td></tr><tr><td>Hard UE Reconnection</td><td>Complete modem restart followed by reinitialization of the UE communication stack.</td><td>UE registration, security procedures, and PDU session re-establishment, accompanied by a pronounced CP signaling burst and temporary UP interruption.</td><td>Device reboot, modem recovery, or power-cycle event.</td></tr><tr><td>Soft UE Reconnection</td><td>UE-initiated NAS deregistration followed by re-registration without restarting the modem.</td><td>Deregistration and registration signaling followed by PDU session re-establishment and temporary UP interruption.</td><td>Software-triggered reconnection, communication stack restart, or remote maintenance.</td></tr><tr><td>PDU Session Reset</td><td>Release and subsequent re-establishment of the PDU session while UE registration is retained.</td><td>PDU session management and NGAP resource signaling, with temporary loss and restoration of UP connectivity.</td><td>Session recovery after maintenance or a transient data-path fault.</td></tr><tr><td>PDU Session Interruption</td><td>Temporary interruption of UP connectivity without a complete UE reconnection or explicit PDU session reset.</td><td>Temporary absence of UP communication and possible CM or PDU resource signaling during interruption and recovery.</td><td>Temporary radio degradation, link outage, or short communication-path disruption.</td></tr></table>

Table 3: Capture-level dataset partitioning

<table><tr><td rowspan="2">Traffic category</td><td colspan="2">Model</td><td rowspan="2">Adapt. Val.</td><td rowspan="2">Test</td><td rowspan="2">Total</td><td rowspan="2">Nom. dur.</td></tr><tr><td>Train</td><td>Val.</td></tr><tr><td>Stable benign</td><td>63</td><td>9</td><td>0</td><td>18</td><td>90</td><td>15.0 h</td></tr><tr><td>Malicious-only</td><td>80</td><td>32</td><td>0</td><td>48</td><td>160</td><td>26.7 h</td></tr><tr><td>Benign variation</td><td>0</td><td>0</td><td>20</td><td>60</td><td>80</td><td>13.3 h</td></tr><tr><td>Mixed variation–attack</td><td>0</td><td>0</td><td>64</td><td>128</td><td>192</td><td>32.0 h</td></tr><tr><td>Overall total</td><td>143</td><td>41</td><td>84</td><td>254</td><td>522</td><td>87.0 h</td></tr></table>

Values without units denote numbers of captures. Adapt., Val., and Nom. dur. denote adaptation, validation, and nominal duration, respectively.

The model development data comprise 90 stable benign captures and 160 malicious-only captures. The malicious captures cover four attack families, four configuration levels, and ten repetitions for each family and level combination Five repetitions are assigned to model training, two to model validation, and three to testing.

The benign variation data extend the collection reported in the preceding study [2] from 40 to 80 captures by adding ten new captures for each of the four connectivity scenarios. Each capture contains two controlled executions of the corresponding connectivity variation. Five captures per scenario are assigned to adaptation validation, and the remaining 15 are reserved for testing.

The mixed variation–attack data comprise all combinations of four connectivity scenarios, four attack families, four attack levels, and three repetitions. One repetition from each combination is assigned to adaptation validation, and two are reserved for testing. The connectivity variation and the attack affect different UEs in every mixed capture. CP indicators are extracted from the signaling trace associated with the UE subjected to the connectivity variation.

## 4.5 CP Context Parameter Selection

The CP context parameters were determined using only the benign variation adaptation validation captures. A sensitivity analysis showed that an internal gap of five TWs was the smallest tested value for which the number of CP activity clusters stabilized. The cluster count remained unchanged for all larger tested gaps. The padding parameters were selected by jointly considering the mean fraction of false positives under the original decision rule covered by the CP context across the four IDS models and the fraction of TWs included in the context. Increasing the post-padding substantially increased false-positive coverage up to seven TWs, while the increase from seven to eight TWs provided only a limited additional gain. A post-padding of seven TWs was therefore selected. With this value fixed, additional pre-padding provided comparatively limited gains in false-positive coverage while further increasing the fraction of TWs included in the context. Pre-padding was therefore set to zero. These parameters were subsequently fixed for all test evaluations.

## 5 Evaluation Results

The four traffic-based IDS models and their original thresholds remain fixed throughout the evaluation. For reference, the frozen models yield FPRs between 4.60% and 4.99% on the stable benign test set from the preceding study [10]. The following analysis examines the increase in FPR under benign connectivity variations, differences in FPR within and outside the CP context, and the trade-off between FPR reduction and retained campaign recall under the proposed CP-aware decision adaptation.

## 5.1 Impact of Benign Connectivity Variations

## 5.1.1 FPR under Benign Variations

Figure 2 compares the FPR of each frozen IDS model on the stable benign test set and the benign variation test set. Benign connectivity variations increase the FPR for all four models. The FPR rises from 4.99% to 7.27% for LogReg, from 4.60% to 5.14% for RF, from 4.86% to 7.59% for SVM, and from 4.95% to 6.73% for XGBoost. The corresponding increases range from 0.54 pp for RF to 2.73 pp for SVM. These results show that legitimate connectivity procedures can shift encrypted UP traffic sufficiently to produce additional false positives.

![](images/6bb8fe687f197457cbe3697a55002cdd1850d9bdcdaa341953417b6b0fe769a8.jpg)  
Figure 2: FPR under stable benign conditions and benign connectivity variations.

Table 4: FPR within and outside the CP context on the benign variation test set.

<table><tr><td>Model</td><td>FPR outside CP context [%]</td><td>FPR inside CP context [%]</td><td>Relative FPR increase [%]</td></tr><tr><td>LogReg</td><td>5.96</td><td>10.79</td><td>81.0</td></tr><tr><td>RF</td><td>4.47</td><td>6.94</td><td>55.0</td></tr><tr><td>SVM</td><td>5.42</td><td>13.42</td><td>147.5</td></tr><tr><td>XGBoost</td><td>5.40</td><td>10.29</td><td>90.4</td></tr></table>

Relative FPR increases are calculated from unrounded values using the FPR outside the CP context as the reference.

## 5.1.2 FPR within and outside the CP Context

The temporal CP context contains 2,206 of the 8,128 TWs in the benign variation test set, corresponding to 27.1% of the evaluated timeline. Table 4 compares the FPR within and outside this context. Although the CP context covers only part of the captures, all four models exhibit substantially higher FPRs within these intervals. Outside the context, the FPR ranges from 4.47% to 5.96%, whereas the corresponding range within the context is 6.94% to 13.42%.

The relative increase ranges from 55.0% for RF to 147.5% for SVM. LogReg and XGBoost also show pronounced increases of 81.0% and 90.4%, respectively. The magnitude differs across models, but the direction of the change remains consistent. This result indicates that false positives under benign connectivity variations are not distributed uniformly over time but are concentrated in intervals temporally associated with CP activity. The observed concentration motivates applying the adapted threshold only within the CP context while retaining the original decision rule outside it.

## 5.2 CP-Aware Adaptation

Table 5 presents the test results for the operating points selected with $\delta _ { \mathrm { v a l } } \in \{ 0 , 0 . 5 , 1 , 2 , 5 \}$ pp. For each operating point, the selected CP-specific threshold is applied only within the CP context, while the original threshold remains active outside it. Global and CP-context FPRs are measured on the benign variation test set, and $\Delta R _ { m , \mathrm { c a m p } } ^ { \mathrm { t e s t } }$ denotes the campaign recall reduction on the mixed variation–attack test set. The RR columns report relative FPR reductions with respect to the original decision rule. SVM thresholds are signed decision-function values and may therefore be negative.

Under the original decision rule, campaign recall on the mixed variation–attack test set is 74.55% for LogReg, 76.38% for RF, 72.24% for SVM, and 81.39% for XGBoost. These values serve as the references for calculating $\bar { \Delta { R } } _ { m , \mathrm { c a m p } } ^ { \mathrm { t e s t } } .$ Since the validation tolerance is applied only during adaptation validation, the campaign recall reduction measured on the test set may exceed the corresponding tolerance. The test results are not used to reselect any threshold.

The results show the same general pattern for all four models. Higher values of $\delta _ { \mathrm { v a l } }$ allow higher CP-specific thresholds, which reduce both global FPR and FPR within the CP context but also increase campaign recall reduction. The FPR reduction is greater within the CP context because the adapted threshold is applied only in these intervals. The CP context covers 27.1% of the benign variation test set, while the original threshold remains active for the other 72.9% of TWs. The unchanged decisions outside the context therefore limit the reduction in global FPR.

Table 5: FPR and campaign recall trade-off on the test sets for CP-aware operating points selected on adaptation validation data

<table><tr><td rowspan="2">Model</td><td rowspan="2"> $\delta_{val}$ (pp)</td><td rowspan="2"> $\Delta R_{m,camp}^{test}$ (pp)</td><td colspan="2">Threshold</td><td colspan="3">Global FPR (%)</td><td colspan="3">FPR within the CP context (%)</td></tr><tr><td> $\tau_m$ </td><td> $\tau_{m,CP}^{(\delta_{val})}$ </td><td>Original</td><td>Adapted</td><td>RR (%)</td><td>Original</td><td>Adapted</td><td>RR (%)</td></tr><tr><td rowspan="5">LogReg</td><td>0</td><td>0.01</td><td>0.4510</td><td>0.4527</td><td>7.27</td><td>7.23</td><td>0.5</td><td>10.79</td><td>10.65</td><td>1.3</td></tr><tr><td>0.5</td><td>0.48</td><td>0.4510</td><td>0.4953</td><td>7.27</td><td>6.98</td><td>4.1</td><td>10.79</td><td>9.70</td><td>10.1</td></tr><tr><td>1</td><td>0.89</td><td>0.4510</td><td>0.5402</td><td>7.27</td><td>6.78</td><td>6.8</td><td>10.79</td><td>8.98</td><td>16.8</td></tr><tr><td>2</td><td>2.27</td><td>0.4510</td><td>0.6746</td><td>7.27</td><td>6.14</td><td>15.6</td><td>10.79</td><td>6.62</td><td>38.7</td></tr><tr><td>5</td><td>5.36</td><td>0.4510</td><td>0.9220</td><td>7.27</td><td>4.95</td><td>32.0</td><td>10.79</td><td>2.22</td><td>79.4</td></tr><tr><td rowspan="5">RF</td><td>0</td><td>0.00</td><td>0.5765</td><td>0.5765</td><td>5.14</td><td>5.14</td><td>0.0</td><td>6.94</td><td>6.94</td><td>0.0</td></tr><tr><td>0.5</td><td>0.41</td><td>0.5765</td><td>0.5975</td><td>5.14</td><td>4.98</td><td>3.1</td><td>6.94</td><td>6.35</td><td>8.5</td></tr><tr><td>1</td><td>0.84</td><td>0.5765</td><td>0.6184</td><td>5.14</td><td>4.86</td><td>5.5</td><td>6.94</td><td>5.89</td><td>15.0</td></tr><tr><td>2</td><td>2.27</td><td>0.5765</td><td>0.6843</td><td>5.14</td><td>4.52</td><td>12.2</td><td>6.94</td><td>4.62</td><td>33.3</td></tr><tr><td>5</td><td>5.65</td><td>0.5765</td><td>0.8330</td><td>5.14</td><td>3.78</td><td>26.6</td><td>6.94</td><td>1.90</td><td>72.5</td></tr><tr><td rowspan="5">SVM</td><td>0</td><td>0.00</td><td>-0.0987</td><td>-0.0987</td><td>7.59</td><td>7.59</td><td>0.0</td><td>13.42</td><td>13.42</td><td>0.0</td></tr><tr><td>0.5</td><td>0.85</td><td>-0.0987</td><td>0.0665</td><td>7.59</td><td>6.75</td><td>11.0</td><td>13.42</td><td>10.34</td><td>23.0</td></tr><tr><td>1</td><td>1.77</td><td>-0.0987</td><td>0.2643</td><td>7.59</td><td>6.18</td><td>18.6</td><td>13.42</td><td>8.20</td><td>38.9</td></tr><tr><td>2</td><td>3.22</td><td>-0.0987</td><td>0.5729</td><td>7.59</td><td>5.68</td><td>25.1</td><td>13.42</td><td>6.39</td><td>52.4</td></tr><tr><td>5</td><td>6.27</td><td>-0.0987</td><td>1.2488</td><td>7.59</td><td>4.72</td><td>37.8</td><td>13.42</td><td>2.86</td><td>78.7</td></tr><tr><td rowspan="5">XGBoost</td><td>0</td><td>0.00</td><td>0.5204</td><td>0.5204</td><td>6.73</td><td>6.73</td><td>0.0</td><td>10.29</td><td>10.29</td><td>0.0</td></tr><tr><td>0.5</td><td>0.48</td><td>0.5204</td><td>0.5914</td><td>6.73</td><td>6.47</td><td>3.8</td><td>10.29</td><td>9.34</td><td>9.3</td></tr><tr><td>1</td><td>1.37</td><td>0.5204</td><td>0.7032</td><td>6.73</td><td>5.91</td><td>12.2</td><td>10.29</td><td>7.25</td><td>29.5</td></tr><tr><td>2</td><td>2.55</td><td>0.5204</td><td>0.8296</td><td>6.73</td><td>5.35</td><td>20.5</td><td>10.29</td><td>5.21</td><td>49.3</td></tr><tr><td>5</td><td>5.91</td><td>0.5204</td><td>0.9813</td><td>6.73</td><td>4.47</td><td>33.6</td><td>10.29</td><td>1.95</td><td>81.1</td></tr></table>

RR denotes the relative FPR reduction with respect to the original decision rule, calculated from unrounded FPR values.

At $\delta _ { \mathrm { v a l } } = 0$ pp, RF, SVM, and XGBoost retain their original thresholds. LogReg uses a slightly higher CP-specific threshold of 0.4527 instead of 0.4510. This operating point reduces global FPR by 0.5% and FPR within the CP context by 1.3%, while campaign recall decreases by only 0.01 pp on the mixed variation–attack test set.

At $\delta _ { \mathrm { v a l } } = 0 . 5$ pp, global FPR is reduced by 3.1–11.0%, and FPR within the CP context is reduced by 8.5–23.0%. The corresponding campaign recall reduction ranges from 0.41 to 0.85 pp. The reduction observed for SVM on the test set exceeds the validation tolerance. At $\delta _ { \mathrm { v a l } } = 1$ pp, global FPR reduction reaches 5.5–18.6%, while FPR reduction within the CP context reaches 15.0–38.9%. Campaign recall reduction ranges from 0.84 to 1.77 pp. The test-set reductions for SVM and XGBoost exceed the validation tolerance. These results confirm that the validation constraint does not provide a guaranteed bound on the test set. The operating points selected at 2 pp follow the same trend, as reported in Table 5.

The largest FPR reductions are obtained at $\delta _ { \mathrm { v a l } } = 5 ~ \mathrm { p p }$ . Global FPR is reduced by 26.6–37.8%, and FPR within the CP context is reduced by 72.5–81.1%. These FPR reductions are accompanied by campaign recall reductions of 5.36–6.27 pp. The operating points therefore provide different choices for deployment rather than one universally preferred threshold. Lower tolerances retain more campaign recall, whereas higher tolerances provide larger reductions in false positives temporally associated with benign connectivity variations.

## 6 Conclusion and Future Work

This paper investigated the effect of benign private 5G connectivity variations on frozen IDS models for encrypted OPC UA traffic. All four models exhibited higher FPRs under connectivity variations than under stable benign conditions. False positives were also more frequent within the temporal CP context, indicating that the increase was concentrated in intervals associated with UE connectivity activity rather than distributed uniformly throughout the captures.

A CP-aware decision adaptation was introduced to address this effect while preserving the underlying traffic-based IDS. Evaluation on the benign variation and mixed variation–attack test captures showed that the method reduces both global FPR and FPR within the CP context. The operating points provide an explicit trade-off between FPR reduction and retained campaign recall. Conservative tolerances preserve most campaign recall while providing moderate FPR reduction, whereas more permissive tolerances achieve substantially larger FPR reductions at the cost of larger campaign recall reductions. The results also show that a recall constraint imposed during validation does not guarantee the same bound on the test data.

The evaluation is limited to four controlled connectivity variations, four OPC UA attack families, and one industrial private 5G testbed. Future work will consider additional connectivity procedures, network configurations, and industrial applications to assess transferability across operating environments. Further work will investigate attacks and connectivity variations affecting the same UE, automated selection of CP context parameters, and procedure- and intensity-aware adaptations that exploit the individual components of the CP context vector while maintaining explicit constraints on campaign recall.

## Acknowledgment

This research is funded by dtec.bw – Digitalization and Technology Research Center of the Bundeswehr. dtec.bw is funded by the European Union – NextGenerationEU (project “Digital Sensor-2-Cloud Campus Platform” (DS2CCP), https://dtecbw.de/home/forschung/hsu/projekt-ds2ccp).

The authors would like to thank J. Jockram and F. Mueller for their valuable support. We also gratefully acknowledge ipoque GmbH, Deutsche Telekom and Ericsson for their continuous support and cooperation.

## References

[1] Toshiaki Honda, Yuki Shimazawa, Takashi Hamaguchi, and Yoshihiro Hashimoto. Monitoring encrypted communication with OPC UA. International Journal ofService and Knowledge Management, 6(2):1–15, 2022 doi:10.52731/ijskm.v6.i2.731.

[2] Song Son Ha, Florian Foerster, Henry Beuster, Tim Kittel, Dominik Merli, and Gerd Scholl. Impact of benign connectivity variations on intrusion detection for encrypted OPC UA traffic in industrial private 5G networks. In 2026 IEEE 31st International Conference on Emerging Technologies and Factory Automation (ETFA), 2026. in press.

[3] Meng Shen, Ke Ye, Xingtong Liu, Liehuang Zhu, Jiawen Kang, Shui Yu, Qi Li, and Ke Xu. Machine learningpowered encrypted network traffic analysis: A comprehensive survey. IEEE Communications Surveys & Tutorials, 25(1):791–824, 2023. doi:10.1109/COMST.2022.3208196.

[4] Il Hwan Ji, Ju Hyeon Lee, Min Ji Kang, Woo Jin Park, Seung Ho Jeon, and Jung Taek Seo. Artificial intelligence based anomaly detection technology over encrypted traffic: A systematic literature review. Sensors, 24(3), 2024. doi:10.3390/s24030898. Art. no. 898.

[5] Navid Malekghaini, Elham Akbari, Mohammad A. Salahuddin, Noura Limam, Raouf Boutaba, Bertrand Mathieu, Stephanie Moteau, and Stéphane Tuffin. Deep learning for encrypted traffic classification in the face of data drift: An empirical study. Computer Networks, 225:109648, 2023. doi:10.1016/j.comnet.2023.109648.

[6] Yuqi Qing, Qilei Yin, Xinhao Deng, Xiaoli Zhang, Peiyang Li, Zhuotao Liu, Kun Sun, Ke Xu, and Qi Li. Training robust classifiers for classifying encrypted traffic under dynamic network conditions. In Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, pages 3564–3578. Association for Computing Machinery, 2025. ISBN 979-8-4007-1525-9. doi:10.1145/3719027.3765073.

[7] Toshiaki Honda, Yuki Shimazawa, Takashi Hamaguchi, and Yoshihiro Hashimoto. Development of a monitoring system for encrypted data by OPC UA. In 2021 10th International Congress on Advanced Applied Informatics (IIAI-AAI), pages 731–736, 2021. doi:10.1109/IIAI-AAI53430.2021.00129.

[8] Charles Varlei Neu, Ina Schiering, and Avelino F. Zorzo. Simulating and detecting attacks of untrusted clients in OPC UA networks. In Proceedings ofthe Third Central European Cybersecurity Conference, pages 11:1–11:6. Association for Computing Machinery, 2019. ISBN 978-1-4503-7296-1. doi:10.1145/3360664.3360675.

[9] Zhangfa Wu, Huifang Li, Yi Hua, Nguyen H. Tran, and Hongping Gan. Frequency-domain anomaly detection for encrypted traffic in industrial control systems. IEEE Transactions on Industrial Informatics, 21(10):7859–7869, 2025. doi:10.1109/TII.2025.3582394.

[10] Song Son Ha, Florian Foerster, Henry Beuster, Eduard Zeller, Dominik Merli, and Gerd Scholl. Residual observability and attack detectability in encrypted OPC UA traffic. In 2026 IEEE 52nd Annual Conference of the IEEE Industrial Electronics Society (IECON), 2026. in press.

[11] Tobias Fritz, Alexander Schwankner, Jan-Hendrik Wissing, Robin Buchta, and Gabi Dreo Rodosek. Granomaly: A framework for anomaly detection in 5G core network control plane traffic with temporal graph neural networks. In NOMS 2025 - 2025 IEEE Network Operations and Management Symposium, pages 1–6, 2025. doi:10.1109/NOMS57970.2025.11073582.

[12] Min Wang, Peng Li, Zhang Cheng, Wenmao Liu, Lei Nie, Haizhou Bao, Qin Liu, and Kai Zhang. Unsupervised graph-sequence anomaly detection for 5G core network control plane traffic. In 2023 IEEE 29th International Conference on Parallel and Distributed Systems (ICPADS), pages 1645–1652, 2023. doi:10.1109/ICPADS60453.2023.00230.

[13] Zixu Tian, Rajendra Patil, Mohan Gurusamy, and Joshua McCloud. ADSeq-5GCN: Anomaly detection from network traffic sequences in 5G core network control plane. In 2023 IEEE 24th International Conference on High Performance Switching and Routing (HPSR), pages 75–82, 2023. doi:10.1109/HPSR57248.2023.10147931.

[14] Haohuang Wen, Phillip A. Porras, Vinod Yegneswaran, and Zhiqiang Lin. A fine-grained telemetry stream for security services in 5G open radio access networks. In Proceedings of the 1st International Workshop on Emerging Topics in Wireless, pages 18–23. Association for Computing Machinery, 2022. ISBN 978-1-4503-9934-0. doi:10.1145/3565474.3569070.

[15] Omer H. Abdelrahman and Erol Gelenbe. A data plane approach for detecting control plane anomalies in mobile networks. In Internet of Things. IoT Infrastructures, volume 169 of Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering, pages 210–221. Springer, 2016. doi:10.1007/978-3-319-47063-4\_19.

[16] Fatemeh Stodt, Christoph Reich, and Fabrice Theoleyre. Context-aware anomaly detection by community detection in the internet of things. Computer Communications, 248:108414, 2026. ISSN 0140-3664. doi:10.1016/j.comcom.2026.108414.

[17] Aafan Ahmad Toor, Jia-Chun Lin, and Ernst Gunnar Gran. UoCAD2: An unsupervised online contextual anomaly detection approach using optimized hyperparameters of RNNs for multivariate time series. Internet ofThings, 33: 101664, 2025. ISSN 2542-6605. doi:10.1016/j.iot.2025.101664.

[18] Rozhin Yasaei, Felix Hernandez, and Mohammad Abdullah Al Faruque. IoT-CAD: Context-aware adaptive anomaly detection in IoT systems through sensor association. In 2020 IEEE/ACM International Conference On Computer Aided Design (ICCAD), pages 1–9, 2020.

[19] Adrian Komadina, Mislav Martinic, Stjepan Groš, and Željka Mihajlovi´ c. Comparing threshold selection methods´ for network anomaly detection. IEEE Access, 12:124943–124973, 2024. doi:10.1109/ACCESS.2024.3452168.

[20] Muhammad Qasim Ali, Ehab Al-Shaer, Hassan Khan, and Syed Ali Khayam. Automated anomaly detector adaptation using adaptive threshold tuning. ACM Trans. Inf. Syst. Secur., 15(4):17:1–17:30, 2013. doi:10.1145/2445566.2445569.

[21] Pedro Gamallo-Fernández, Alexandre Cabodevila, Juan Carlos Vidal, and Manuel Lama. Detecting anomalous patterns in process executions. Computing, 108, 2026. doi:10.1007/s00607-025-01604-x. Art. no. 19.

[22] Dariusz Zelasko. Cost-aware network traffic anomaly detection with histogram-based gradient boosting.<sup>˙</sup> Applied Sciences, 16(7), 2026. doi:10.3390/app16073496. Art. no. 3496.

[23] Johannes vom Dorp, Sven Merschjohann, David Meier, Florian Patzer, Markus Karch, and Christian Haas. OPC UA security analysis. Federal Officefor Information Security (BSI), 2022.

[24] Song Son Ha, Florian Foerster, Thomas Robert Doebbert, Tim Kittel, Dominik Merli, and Gerd Scholl. Testbed and software architecture for enhancing security in industrial private 5G networks. In 2025 IEEE 30th International Conference on Emerging Technologies and Factory Automation (ETFA), pages 1–4, 2025. doi:10.1109/ETFA65518.2025.11205743.

[25] Real Games. Factory I/O: 3D factory simulation software. Software, 2026. URL https://factoryio.com/. Accessed: Jan. 2026.

[26] Claroty Team82. OPC-UA exploitation framework. Online repository, 2023. URL https://github.com/ claroty/opcua-exploit-framework. Accessed: Dec. 2025.