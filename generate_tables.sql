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
    filename VARCHAR(50),
    time REAL,
    cadenceno INTEGER,
    init_flux_pl NUMERIC(30,15),
    init_flux_pl_err NUMERIC(30,15),
    model_lc_pl NUMERIC(30,15),
    residual_flux NUMERIC(30,15),
    residual_flux_err NUMERIC(30,15),
    PRIMARY KEY (filename, time),
    FOREIGN KEY (filename)
        REFERENCES files (filename)
);

CREATE TABLE dv_defaults
(
    filename VARCHAR(50),
    name VARCHAR(12),
    value VARCHAR(10),
    PRIMARY KEY (filename, name),
    FOREIGN KEY (filename)
        REFERENCES files (filename)
);