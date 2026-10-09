# DeepGBM

Canonical citation key: `ke2019deepgbm`. Verified 2026-09-19.

Official KDD page: https://www.kdd.org/kdd2019/accepted-papers/view/deepgbm-a-deep-learning-framework-distilled-by-gbdt-for-online-prediction-t . It identifies the title, authors and abstract. Author implementation: https://github.com/motefly/DeepGBM . Its README supplies the KDD 2019 citation and pages 384-394.

Supported facts: the official abstract combines CatNN for sparse categorical features with GBDT2NN for numerical features distilled from GBDT, supporting online updates for tabular prediction. In the author code `train_models.py`, `train_GBDT2NN` and `train_DEEPGBM` construct leaf-based embedding targets, then train neural models using those targets. This is relevant prior art for tree-to-neural representation transfer. It does not evaluate the Tor-presence task or the present grouped background-tail protocol.
