CREATE TABLE files
(
    filename VARCHAR(20),
    datetime TIMESTAMP,
    PRIMARY KEY (filename)
);

CREATE TABLE defaults
(
    kepler_id INTEGER,
    quarter INTEGER,
    name VARCHAR(12),
    value VARCHAR(10),
    PRIMARY KEY (kepler_id, quarter)
) ;

CREATE TABLE data
(
    kepler_id INTEGER,
    quarter INTEGER,
    time REAL,
    time_bjd REAL,
    timecorr REAL,
    cadenceno INTEGER,
    sap_flux REAL,
    sap_flux_err REAL,
    sap_bkg REAL,
    sap_bkg_err REAL,
    pdcsap_flux REAL,
    pdcsap_flux_err REAL,
    sap_quality INTEGER,
    psf_centr1 REAL,
    psf_centr1_err REAL,
    psf_centr2 REAL,
    psf_centr2_err REAL,
    mom_centr1 REAL,
    mom_centr1_err REAL,
    mom_centr2 REAL,
    mom_centr2_err REAL,
    pos_corr1 REAL,
    pos_corr2 REAL,
    PRIMARY KEY (kepler_id, quarter, time),
    FOREIGN KEY (kepler_id, quarter)
        REFERENCES defaults (kepler_id, quarter)
);