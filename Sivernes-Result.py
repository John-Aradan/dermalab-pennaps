from RF_crossval_Siverence_Test import get_siverence

Dict = {
    'erythema': 2,
    'scaling': 2,
    'definite_borders': 0,
    'itching': 3,
    'koebner_phenomenon': 0,
    'polygonal_papules': 0,
    'follicular_papules': 0,
    'oral_mucosal_involvement': 0,
    'knee_and_elbow_involvement': 1,
    'scalp_involvement': 0,
    'family_history': 0,
    'melanin_incontinence': 0,
    'eosinophils_infiltrate': 0,
    'PNL_infiltrate': 0,
    'fibrosis_papillary_dermis': 3,
    'exocytosis': 2,
    'acanthosis': 0,
    'hyperkeratosis': 0,
    'parakeratosis': 0,
    'clubbing_rete_ridges': 0,
    'elongation_rete_ridges': 0,
    'thinning_suprapapillary_epidermis': 0,
    'spongiform_pustule': 0,
    'munro_microabcess': 0,
    'focal_hypergranulosis': 0,
    'disappearance_granular_layer': 0,
    'vacuolisation_damage_basal_layer': 0,
    'spongiosis': 3,
    'saw_tooth_appearance_retes': 0,
    'follicular_horn_plug': 0,
    'perifollicular_parakeratosis': 0,
    'inflammatory_mononuclear_infiltrate': 0,
    'band_like_infiltrate': 1,
    'age': 55
}

pred = get_siverence(Dict)
print(pred[0])