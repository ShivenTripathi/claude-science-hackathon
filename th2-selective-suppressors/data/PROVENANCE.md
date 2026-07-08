# Data provenance

These files are PUBLIC supplementary tables / reference signatures, redistributed for
reproducibility with attribution. They are NOT original to this project.

- `Ota_Th2vsTh1_DE_results.csv`, `Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv`,
  `*_vs_Th0_DE_results.csv`, `combined_Th2_vs_Th1_signature.csv`, `DE_stats.suppl_table.csv`,
  `guide_kd_efficiency.suppl_table.csv`, `polarization_prediction_condition_comparison_regulator_coefficients.csv`,
  `th1_th2_known_regulators.yaml`, `Lambert_2018_HumanTF.csv`, `donor_info.csv`
  → from Zhu R., Dann E. et al. 2025 (bioRxiv 2025.12.23.696273),
    https://github.com/emdann/GWT_perturbseq_analysis_2025 and the public S3 bucket
    s3://genome-scale-tcell-perturb-seq/marson2025_data/ . Ota-2021 signature per that repo.

The 16.8 GB DE matrix (GWCD4i.DE_stats.h5ad) is intentionally NOT vendored; the code streams it
from the public bucket. See each source's license/citation before reuse.
