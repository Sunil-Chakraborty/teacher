import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Load the data
# Note: Replace with your actual file path
# df = pd.read_csv('catg_jrnl_pub1.csv')

# For this example, I'll create the dataframe from the provided data
data = [
    [2019, "Working Memory Modeling Using Inverse Fuzzy Relational Approach", 3, "Corresponding author", "Applied Soft Computing, Elsevier", "UGC Care List", 5.472, 35],
    [2016, "Prediction of Protein-Protein Interaction Network using a Multi-Objective Optimization Approach", 3, "Corresponding author", "Journal of Bioinformatics and Computational Biology", "UGC Care List", 0.8, 35],
    [2015, "Extending Multi-objective Differential Evolution for Optimization in Presence of Noise", 2, "First and Corresponding author", "Information Sciences, Elsevier", "UGC Care List", 3.5, 35],
    [2017, "Near-field effects on site characterization using MASW Technique", 2, "First author", "Soil Dynamics and Earthquake Engineering", "UGC Care List", 4.25, 31],
    [2016, "A Type-2 Fuzzy Classifier for Gesture Induced Pathological Disorder Recognition", 3, "First and Corresponding author", "Fuzzy Sets and Systems, Elsevier", "UGC Care List", 2.6, 35],
    [2011, "Research", 2, "First author", "fsfa", "UGC Care List", 0.5, 25],
    [2016, "Non-dominated Sorting Bee Colony Optimization in Presence of Noise", 2, "First and Corresponding author", "Soft Computing, Springer", "UGC Care List", 1.8, 35],
    [2016, "A Modified Imperialist Competitive Algorithm for Multi-Robot Stick-Carrying Application", 3, "Other", "Robotics and Autonomous Systems, Elsevier", "UGC Care List", 2.6, 35],
    [2017, "Evolutionary Perspective for Optimal Selection of EEG Electrodes and Features", 3, "Corresponding author", "Biomedical Signal Processing and Control, Elsevier", "UGC Care List", 3.063, 35],
    [2015, "Differential Evolution for Noisy Multi-objective Optimization", 2, "First and Corresponding author", "Artificial Intelligence, Elsevier", "UGC Care List", 3.7, 35],
    [2018, "Realization of Learning Induced Self-Adaptive Sampling in Noisy Optimization", 2, "First and Corresponding author", "Applied Soft Computing, Elsevier", "UGC Care List", 4.873, 35],
    [2017, "Noisy Evolutionary Optimization Algorithms – A Comprehensive Survey", 3, "First and Corresponding author", "Swarm and Evolutionary Computation, Elsevier", "UGC Care List", 3.818, 35],
    [2019, "Hemodynamic Analysis for Cognitive Load Assessment and Classification in Motor Learning Tasks Using Type-2 Fuzzy Sets", 4, "Corresponding author", "IEEE Transactions on Emerging Topics in Computational Intelligence", "UGC Care List", 4.2, 35],
    [2018, "Ballet E-Learning Using Fuzzy Set Induced Posture Recognition by Piece-Wise Linear Approximation of Connected Components", 3, "Corresponding author", "Applied Soft Computing, Elsevier", "UGC Care List", 4.873, 35],
    [2019, "Uncertainty Management by Feature Space Tuning for Single-trial P300 Detection", 4, "Other", "International Journal of Fuzzy Systems, Springer", "UGC Care List", 3.7, 35],
    [2020, "Quantitative insights into the crystal structure of a mixed-ligand Co(III) complex: Experimental and theoretical studies", 4, "Corresponding author", "Journal of Molecular Structure", "UGC Care List", 3.841, 36],
    [2020, "Diverse structural assemblies of a series of ninhydrin derivatives: Quantitative analyses from experimental and theoretical studies", 5, "Corresponding author", "Journal of Molecular Structure", "UGC Care List", 3.841, 36],
    [2020, "Supramolecular assemblies involving salt bridges: DFT and X-ray evidence of bipolarity", 6, "Corresponding author", "CrystEngComm", "UGC Care List", 3.756, 36],
    [2020, "Novel Pb(II) Complexes: X-Ray Structures, Hirshfeld Surface Analysis and DFT Calculations", 5, "Other", "Crystals", "UGC Care List", 2.67, 36],
    [2021, "Anion-dependent structural variations and charge transport property analysis of 4′-(3-pyridyl)-4,2′:6′,4′′-terpyridinium salts", 7, "Other", "CrystEngComm", "UGC Care List", 3.756, 36],
    [2021, "Active Bromoaniline–Aldehyde Conjugate Systems and Their Complexes as Versatile Sensors of Multiple Cations with Logic Formulation and Efficient DNA/HSA-Binding Efficacy: Combined Experimental and Theoretical Approach", 9, "Other", "ACS Omega", "UGC Care List", 4.132, 36],
    [2020, "In vitro anthelmintic activities of stem and root barks extracts of Parkia biglobosa on infective larvae and adult of Haemonchus contortus", 15, "First author", "African Journal of Biotechnology", "UGC Care List", 0, 25],
    [2022, "Ionic Liquid–Based Pretreatment of Lignocellulosic Biomass for Bioconversion: a Critical Review", 2, "First and Corresponding author", "BioEnergy Research", "UGC Care List", 3.852, 40],
    [2022, "pH-induced structural variations of two new Mg(II)-PDA complexes: experimental and theoretical studies", 5, "Corresponding author", "Journal of Molecular Structure", "UGC Care List", 3.841, 36],
    [2023, "Intriguing π-interactions involving aromatic neutrals, aromatic cations and semiconducting behavior in a pyridinium-carboxylate salt", 5, "Corresponding author", "Journal of Molecular Structure", "UGC Care List", 3.841, 36],
    [2022, "Exploring Solid-State Supramolecular Architectures of Penta(carboxymethyl)diethylenetriamine: Experimental Observation and Theoretical Studies", 5, "Corresponding author", "ChemistrySelect", "UGC Care List", 2.307, 36],
    [2023, "Helical coordination complex of Hg(ClO4)2 with bulky hydrazine derivative: A Möbius-like discrete metal chelate", 7, "Corresponding author", "Inorganic Chemistry Communications", "UGC Care List", 3.428, 36],
    [2022, "Parametric Optimization and Kinetics Study of Effective Removal of Methylene Blue by Citric Acid Modified Arjun Bark Powder", 2, "First and Corresponding author", "Biomass Conversion and Biorefinery", "UGC Care List", 4.05, 40],
    [2021, "Supramolecular association and quantification of intermolecular interactions of 4′-functionalized 2,2′:6′,2″-terpyridines: Experimental observation and theoretical studies", 4, "Corresponding author", "Journal of Molecular Structure", "UGC Care List", 3.841, 36],
    [2021, "A combined experimental and theoretical analysis on the solid-state supramolecular assemblies of pent‑2-ynol derivatives", 6, "Corresponding author", "Journal of Molecular Structure", "UGC Care List", 3.841, 36],
    [2022, "Structural elucidation of phenoxybenzaldehyde derivatives from laboratory powder X-ray diffraction: A combined experimental and theoretical quantum mechanical study", 4, "Corresponding author", "Journal of Molecular Structure", "UGC Care List", 3.841, 36],
    [2023, "Quantitative analysis of intermolecular interactions in crystalline substituted triazoles", 4, "Corresponding author", "Journal of Molecular Structure", "UGC Care List", 3.841, 36],
    [2023, "La-doped LiMnPO4/C cathode material for Lithium-ion battery", 2, "Corresponding author", "Chemical Engineering Science", "UGC Care List", 4.889, 40],
    [2022, "Kinetics study of catalytic wet oxidation of phenol over novel ceria promoted mesoporous silica supported Ru-Fe3O4 catalyst", 2, "First and Corresponding author", "Chemical Engineering Research and Design", "UGC Care List", 4.119, 40],
    [2022, "Enhancement of Li+ ion kinetics in boehmite nanofiber coated polypropylene separator in LiFePO4 cells", 4, "Corresponding author", "Journal of Solid State Chemistry", "UGC Care List", 3.656, 40],
    [2022, "Iron Oxide- and Copper Oxide-Decorated Chemically Reduced Graphene Oxide Composite as a Novel Electrode for Hybrid Supercapacitors", 4, "First author", "Energy & Fuels", "UGC Care List", 5.3, 38],
    [2022, "Fractional PIλDµ controller design for non-linear PEM fuel cell for pressure control based on a genetic algorithm", 4, "Corresponding author", "Indian Chemical Engineer", "UGC Care List", 1.5, 38],
    [2022, "Synthesis of advanced multifunctional biopolymeric membrane via emulsion templating method", 3, "Corresponding author", "Materials Today: Proceedings", "UGC Care List", 0, 38],
    [2020, "Ammonia-salt solvent promotes cellulosic biomass deconstruction under ambient pretreatment conditions to enable rapid soluble sugar production at ultra-low enzyme loadings", 11, "Other", "Green Chemistry", "UGC Care List", 11.034, 40],
    [2022, "Selective CO2 reduction to methane catalyzed by mesoporous Ru-Fe3O4/CeOx-SiO2 in a fixed bed flow reactor", 9, "First and Corresponding author", "Molecular Catalysis", "UGC Care List", 5.089, 40],
    [2016, "Protein-Protein Interaction Network Prediction Using Stochastic Learning Automata Induced Differential Evolution", 3, "Corresponding author", "Applied Soft Computing, Elsevier", "UGC Care List", 3.6, 35],
    [2017, "A study on surface wave dispersion due to the effect of soft layer in layered media", 3, "First author", "Geomechanics and Engineering", "UGC Care List", 3.2, 31],
    [2021, "Transformation of Wurtzite ZnO to a New Triclinic Nanoporous ZnO Phase via Hydrothermal Treatment with Metformin for Designing Proton Conducting Material", 6, "Other", "Chemistry - An Asian Journal", "UGC Care List", 4.839, 40],
    [2018, "Effect of uncertainty in VS−N correlations on seismic site response analysis", 4, "First author", "Journal of Earth System and Science", "UGC Care List", 1.91, 31],
    [2018, "Effect of Data Uncertainty and Inversion Non-Uniqueness of Surface Wave Tests on VS,30 Estimation", 2, "First and Corresponding author", "Soil dynamics and Earthquake Engineering", "UGC Care List", 4.25, 31],
    [2018, "Kinetic Study of Biogas Recovery from Thermo-chemically Pre-treated Rice Husk", 3, "Corresponding author", "Indian Chemical Engineer", "UGC Care List", 1.091, 40],
    [2018, "Local Site Effect Due to Past Earthquakes in Kolkata", 4, "Other", "Journal of Geological Society of India", "UGC Care List", 1.47, 31],
    [2020, "Influence of Trapped Soft/ Stiff Soil Layer in Seismic Site Response Analysis", 3, "First and Corresponding author", "Journal of Earth System and Science", "UGC Care List", 1.9, 31],
    [2020, "Mapping Surface Wave Dispersion Uncertainty in Vs Profiles to VS,30 and Site Response Analysis", 2, "First and Corresponding author", "Soil dynamics and Earthquake Engineering", "UGC Care List", 4.25, 31],
    [2020, "Prediction of peak ground acceleration for Himalayan region using artificial neural network and genetic algorithm", 3, "Other", "Arabian Journal of Geosciences", "UGC Care List", 1.83, 31],
    [2018, "Seismic Magnitude Conversion Problem", 8, "Other", "Bulletin of Seismological Society of America", "UGC Care List", 3.14, 31],
    [2018, "A generalized Vs-N correlation using various regression analysis and genetic algorithm", 2, "Other", "Acta Geodaetica et Geophysica", "UGC Care List", 1.77, 31],
    [2020, "Surface Wave Dispersion in a Vertically Layered Medium for Varying Subsurface Scenarios", 3, "First and Corresponding author", "International Journal of Geotechnical Earthquake Engineering", "UGC Care List", 0, 31],
    [2022, "A new strategy to fabricate SnS-SnO2 heterostructure with excellent photoresponse and charge transport properties: Efficient photocatalyst for fast photoreduction of Cr(VI)", 5, "Other", "Materials Science and Engineering: B", "UGC Care List", 3.407, 49],
    [2022, "LaNiO3/g-C3N4nanocomposite: An efficient Z-scheme photocatalyst for wastewater treatment using direct sunlight", 12, "Other", "Journal of Rare Earths", "UGC Care List", 4.632, 49],
    [2022, "Tetraphenylporphyrin Decorated Bi2MoO6Nanocomposite: Its Twin Affinity of Oxygen Reduction Reaction and Electrochemical Detection of 4-Nitrophenol", 8, "Corresponding author", "Inorganic Chemistry", "UGC Care List", 5.436, 49],
    [2021, "Facile synthesis of CuCr2O4/BiOBr nanocomposite and its photocatalytic activity towards RhB and tetracycline hydrochloride degradation under household visible LED light irradiation", 12, "Other", "Journal of Alloys and Compounds", "UGC Care List", 6.371, 49],
    [2021, "Hierarchical copper oxide as efficient enzymeless amperometric biosensor and promising photocatalyst", 4, "First author", "Journal of Environmental Chemical Engineering", "UGC Care List", 7.968, 49],
    [2020, "On the properties of dissipative   shocks   in   the   relativistic   accretion   flows.", 2, "First and Corresponding author", "Monthly   Notices   of   the   Royal   Astronomical Society(MNRAS)", "UGC Care List", 5.235, 52],
    [2020, "Degradation of Air Quality (PM10) with Seasonal Change and Health Risk Assessment in Metro City Kolkata", 4, "Other", "International Journal of Advancement in Life Sciences Research", "Other reputed journal as notified by UGC", 0, 66],
    [2017, "Evaluation of anti-inflammatory and antinociceptive activity of methanol extract of Calotropis gigantea root", 6, "Other", "International Journal of Green Pharmacy", "Other reputed journal as notified by UGC", 0, 64],
    [2022, "Analysis of geometrical shape impact on thermal management of practical fluids using square and circular cavities", 4, "Corresponding author", "The European Physical Journal Special Topics", "UGC Care List", 2.6, 68],
    [2021, "Exact solutions of fluid flow in an axially oscillating cylindrical pipe and annulus", 2, "Corresponding author", "SN Applied Sciences", "UGC Care List", 2.6, 68],
    [2020, "A Triangular Common Subexpression Elimination Algorithm with Reduced Logic Operators in FIR Filter", 2, "Corresponding author", "IEEE Transactions on Circuits and Systems-II: Express Briefs", "UGC Care List", 4.4, 81],
    [2016, "Modelling the 21-cm Signal from the Epoch of Reionization and Cosmic Dawn", 8, "Other", "Journal of Astrophysics and Astronomy", "UGC Care List", 1.5, 69],
    [2014, "PRAKRITI, BIBHUTIBHUSHAN O RADDI PATHAKER KECCHA", 1, "First and Corresponding author", "ASHOKNAGAR", "Other reputed journal as notified by UGC", 0, 82],
    [2020, "Nitikathayam\nBharatiya Samskritermulanusandhanam", 1, "First and Corresponding author", "Anviksa (ISSN: 0587-1646) Research Journal of the Department of Sanskrit, (Refereed Journal) J.U.", "Other reputed journal as notified by UGC", 0, 89],
    [2021, "Contrasting spectroscopic response of human hemoglobin in presence of graphene oxides and its reduced form: Comparative approach with carbon quantum dots", 10, "Other", "SpectrochimicaActa Part A: Molecular and Biomolecular Spectroscopy", "UGC Care List", 4.831, 49],
    [2021, "An Efficient Data Routing Scheme for Multi-patient Monitoring in a Biomedical Sensor Network through Energy Equalization Strategy", 3, "Other", "Wireless Networks", "UGC Care List", 3, 81],
    [2016, "Probing Individual Sources during Reionization and Cosmic Dawn using Square Kilometre Array HI 21-cm Observations", 7, "First and Corresponding author", "Journal of Astrophysics and Astronomy", "UGC Care List", 1.5, 69],
    [2023, "Sustainable Synthesis of α‐Hydroxycarboxylic Acids by Manganese Catalyzed Acceptorless Dehydrogenative Coupling of Ethylene Glycol and Primary Alcohols", 4, "First author", "Angewandte Chemie", "UGC Care List", 16.823, 62],
    [2019, "Particulate Matter And Its Influence On Air Quality For Mumbai And Agra", 5, "First author", "Indian Journal of Environmental Protection", "UGC Care List", 0, 66],
    [2014, "RUPAKER KAVITA BOLA", 1, "First and Corresponding author", "PATHAKI KAVITA", "Other reputed journal as notified by UGC", 0, 82],
    [2022, "Prachinabharate Manavadhikar(a)bhavanayah Tattvanvesanam", 1, "First and Corresponding author", "Vyasashrih", "UGC Care List", 0, 89],
    [2021, "Protease targeted COVID-19 drug discovery: What we have learned from the past SARS-CoV inhibitors?", 4, "Corresponding author", "European Journal of Medicinal Chemistry", "UGC Care List", 6.7, 65],
    [2021, "Identification of molecular fingerprints of natural products for the inhibition of breast cancer resistance protein (BCRP)", 4, "Corresponding author", "Phytomedicine", "UGC Care List", 7.9, 65],
    [2018, "A review on camptothecin analogs with promising cytotoxic profile", 4, "Corresponding author", "Anti-Cancer Agents in Medicinal Chemistry (Formerly Current Medicinal Chemistry-Anti-Cancer Agents)", "UGC Care List", 2.8, 65],
    [2018, "Monte Carlo based modelling approach for designing and predicting cytotoxicity of 2-phenylindole derivatives against breast cancer cell line MCF7", 8, "Corresponding author", "Toxicology in Vitro", "UGC Care List", 3.2, 65],
    [2022, "Magneto-thermal convection of hybrid nanofluid in a non-Darcian porous complex wavy enclosure", 5, "Corresponding author", "The European Physical Journal Special Topics", "UGC Care List", 2.6, 68],
    [2021, "Magnetohydrodynamic bioconvection of oxytactic microorganisms in porous media saturated with Cu-water nanofluid", 4, "First author", "International Journal of Numerical Methods for Heat & Fluid Flow", "UGC Care List", 3.924, 68],
    [2021, "A Survey of FIR Filter Design Techniques: Low-complexity, Narrow Transition-band and Varibale Bandwidth", 2, "Corresponding author", "Integration, the VLSI Journal", "UGC Care List", 1.9, 81],
    [2020, "Fabrication of n-TiO2/p-CuO thin-film heterojunction for efficient photocatalytic degradation of toxic organic dyes and reduction of metal ions in solution", 4, "Other", "Journal of Materials Science: Materials in Electronics", "UGC Care List", 2.779, 49],
    [2020, "Prediction of first higher order modal field for graded index fiber in presence of Kerr nonlinearity", 3, "Corresponding author", "Journal of Optical Communications", "Other reputed journal as notified by UGC", 0, 54],
    [2021, "Monte Carlo Optimization-Based QSAR Study of Some Indole-Based Mcl-1 Inhibitors", 5, "Corresponding author", "International Journal of Quantitative Structure-Property Relationships (IJQSPR)", "UGC Care List", 0, 65],
    [2022, "Thermo-fluidic transport process in a novel M-shaped cavity packed with non-Darcian porous medium and hybrid nanofluid: Application of artificial neural network (ANN)", 6, "Corresponding author", "Physics of Fluids", "UGC Care List", 4.6, 68],
    [2021, "Thermo-bioconvection of oxytactic microorganisms in porous media in the presence of magnetic field", 5, "First author", "International Journal of Numerical Methods for Heat & Fluid Flow", "UGC Care List", 3.924, 68],
    [2021, "A Smart Spectrum Utilization Approach using Multiantenna-based Cognitive Relays in Cognitive Radio Network", 4, "Corresponding author", "International Journal of Communication Systems", "UGC Care List", 2.1, 81],
    [2016, "Redshifted HI 21-cm Signal from the Post-Reionization Epoch: Cross-Correlations with Other Cosmological Probes", 5, "Other", "Journal of Astrophysics and Astronomy", "UGC Care List", 1.5, 69],
    [2015, "SEVABE ATITHISEBAGULI / JEVABE MAYUR KHULE PORRE : SWADESH SENER KAVITA UTHON", 1, "First and Corresponding author", "GRANTHI", "Other reputed journal as notified by UGC", 0, 82],
    [2020, "Visible-light active electrochemically deposited tin selenide thin films: synthesis, characterization and photocatalytic activity", 5, "Other", "Journal of Materials Science: Materials in Electronics", "UGC Care List", 2.779, 49],
    [2022, "Updated chemical scaffolds of ABCG2 inhibitors and their structure-inhibition relationships for future development", 4, "Corresponding author", "European Journal of Medicinal Chemistry", "UGC Care List", 6.7, 65],
    [2021, "First structure–activity relationship analysis of SARS-CoV-2 virus main protease (Mpro) inhibitors: an endeavor on COVID-19 drug discovery", 6, "Corresponding author", "Molecular diversity", "UGC Care List", 3.8, 65],
    [2020, "Good and bad molecular fingerprints for human rhinovirus 3C protease inhibition: Identification, validation, and application in designing of new inhibitors through Monte Carlo-based QSAR study", 5, "Corresponding author", "Journal of Biomolecular Structure and Dynamics", "UGC Care List", 4.4, 65],
    [2020, "Exploring indole derivatives as myeloid cell leukaemia-1 (Mcl-1) inhibitors with multi-QSAR approach: a novel hope in anti-cancer drug discovery", 5, "Corresponding author", "New Journal of Chemistry", "UGC Care List", 3.3, 65],
    [2018, "Identification of molecular fingerprints of phenylindole derivatives as cytotoxic agents: a multi-QSAR approach", 6, "Corresponding author", "Structural Chemistry", "UGC Care List", 1.7, 65],
    [2019, "Optimal bidding in emission constrained economic dispatch", 2, "First author", "International Journal of Environmental Science and Technology", "UGC Care List", 3.519, 78],
    [2018, "First report on the validated classification-based chemometric modeling of human rhinovirus 3C Protease (HRV 3Cpro) inhibitors", 4, "Corresponding author", "International Journal of Quantitative Structure-Property Relationships (IJQSPR)", "UGC Care List", 0, 65],
    [2023, "Hybrid nanofluid magnetohydrodynamic mixed convection in a novel W-shaped porous system", 5, "Corresponding author", "Int. J. Numer. Meth. Heat Fluid Flow", "UGC Care List", 3.924, 68],
    [2022, "Positional impacts of partial wall translations on hybrid nanofluid flow in porous media: Real Coded Genetic Algorithm (RCGA)", 5, "Corresponding author", "International Journal of Mechanical Sciences", "UGC Care List", 7.3, 68]
]

columns = ["Year Of Publication", "Title of the Paper", "No.of authors", "Role of Applicant", 
           "Journal Name", "Jrnl_type", "Imp_factor", "Applicant ID"]

df = pd.DataFrame(data, columns=columns)

# Clean data
df['Imp_factor'] = pd.to_numeric(df['Imp_factor'], errors='coerce')
df['Year Of Publication'] = pd.to_numeric(df['Year Of Publication'], errors='coerce')
df['No.of authors'] = pd.to_numeric(df['No.of authors'], errors='coerce')

# Set up the plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create comprehensive analysis

def create_analysis():
    """
    Comprehensive analysis of journal publication data
    """
    
    print("=" * 80)
    print("JOURNAL PUBLICATION ANALYSIS REPORT")
    print("=" * 80)
    print()
    
    # 1. Basic Statistics
    print("1. BASIC STATISTICS")
    print("-" * 30)
    print(f"Total Publications: {len(df)}")
    print(f"Number of Faculty Members: {df['Applicant ID'].nunique()}")
    print(f"Year Range: {df['Year Of Publication'].min()} - {df['Year Of Publication'].max()}")
    print(f"Average Impact Factor: {df['Imp_factor'].mean():.3f}")
    print(f"Total Impact Factor Score: {df['Imp_factor'].sum():.3f}")
    print()
    
    # 2. Publications by Year
    print("2. PUBLICATIONS BY YEAR")
    print("-" * 30)
    year_counts = df['Year Of Publication'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f"{year}: {count} publications")
    print()
    
    # 3. Top Performers by Applicant
    print("3. TOP PERFORMERS (by Total Publications)")
    print("-" * 50)
    applicant_stats = df.groupby('Applicant ID').agg({
        'Title of the Paper': 'count',
        'Imp_factor': ['sum', 'mean']
    }).round(3)
    applicant_stats.columns = ['Total_Publications', 'Total_Impact_Factor', 'Avg_Impact_Factor']
    applicant_stats = applicant_stats.sort_values('Total_Publications', ascending=False)
    print(applicant_stats.head(10))
    print()
    
    # 4. Journal Type Analysis
    print("4. JOURNAL TYPE ANALYSIS")
    print("-" * 30)
    journal_type_stats = df.groupby('Jrnl_type').agg({
        'Title of the Paper': 'count',
        'Imp_factor': ['sum', 'mean']
    }).round(3)
    journal_type_stats.columns = ['Count', 'Total_Impact', 'Avg_Impact']
    print(journal_type_stats)
    print()
    
    # 5. Role Analysis
    print("5. ROLE DISTRIBUTION")
    print("-" * 30)
    role_counts = df['Role of Applicant'].value_counts()
    for role, count in role_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{role}: {count} ({percentage:.1f}%)")
    print()
    
    # 6. Collaboration Analysis
    print("6. COLLABORATION ANALYSIS")
    print("-" * 30)
    author_stats = df['No.of authors'].describe()
    print(f"Average number of authors per paper: {author_stats['mean']:.2f}")
    print(f"Most collaborative paper: {author_stats['max']} authors")
    print(f"Solo papers: {len(df[df['No.of authors'] == 1])}")
    print()
    
    # 7. High Impact Publications
    print("7. HIGH IMPACT PUBLICATIONS (Impact Factor > 5.0)")
    print("-" * 60)
    high_impact = df[df['Imp_factor'] > 5.0].sort_values('Imp_factor', ascending=False)
    if len(high_impact) > 0:
        for idx, row in high_impact.iterrows():
            print(f"IF: {row['Imp_factor']:.3f} | Year: {row['Year Of Publication']} | Applicant: {row['Applicant ID']}")
            print(f"   {row['Title of the Paper'][:80]}...")
            print()
    else:
        print("No publications with impact factor > 5.0")
    
    # 8. Publisher Analysis
    print("8. TOP PUBLISHERS")
    print("-" * 30)
    #publishers = df['Journal Name'].str.extract(r', (.*?)
    publishers = df['Journal Name'].str.extract(r', (.*)')