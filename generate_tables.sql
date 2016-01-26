CREATE TABLE files
(
    filename VARCHAR(50),
    datetime TIMESTAMP,
    PRIMARY KEY (filename)
);

CREATE TABLE time_defaults
(
    filename VARCHAR(50),
    name VARCHAR(12),
    value VARCHAR(10),
    PRIMARY KEY (filename, name),
    FOREIGN KEY (filename)
        REFERENCES files (filename)
);

CREATE TABLE time_data
(
    -- PRECISE, DECIMALS RELEVANT
    filename VARCHAR(50),
    time NUMERIC(30, 15),
    time_bjd NUMERIC(30, 15),
    timecorr NUMERIC(30, 15),
    cadenceno INTEGER,
    sap_flux NUMERIC(30, 15),
    sap_flux_err NUMERIC(30, 15),
    sap_bkg NUMERIC(30, 15),
    sap_bkg_err NUMERIC(30, 15),
    pdcsap_flux NUMERIC(30, 15),
    pdcsap_flux_err NUMERIC(30, 15),
    sap_quality INTEGER,
    psf_centr1 NUMERIC(30, 15),
    psf_centr1_err NUMERIC(30, 15),
    psf_centr2 NUMERIC(30, 15),
    psf_centr2_err NUMERIC(30, 15),
    mom_centr1 NUMERIC(30, 15),
    mom_centr1_err NUMERIC(30, 15),
    mom_centr2 NUMERIC(30, 15),
    mom_centr2_err NUMERIC(30, 15),
    pos_corr1 NUMERIC(30, 15),
    pos_corr2 NUMERIC(30, 15),
    PRIMARY KEY (filename, time),
    FOREIGN KEY (filename)
        REFERENCES files (filename)
);

CREATE TABLE dv_data
(
    -- PRECISE, DECIMALS RELEVANT
    filename VARCHAR(50)
    TIME REAL,
    CADENCE_NUMBER INTEGER,
    INIT_FLUX_PL NUMERIC(30,15),
    INIT_FLUX_PL_ERR NUMERIC(30,15),
    MODEL_LC_PL NUMERIC(30,15),
    RESIDUAL_FLUX NUMERIC(30,15),
    RESIDUAL_FLUX_ERR NUMERIC(30,15),
    PRIMARY KEY (filename, time),
    FOREIGN KEY (filename)
        REFERENCES files (filename)
);
