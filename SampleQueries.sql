SELECT time, sap_flux 
FROM data INNER JOIN defaults ON
    (data.filename = defaults.filename)
WHERE defaults.name = 'QUARTER' 
    AND defaults.value = '1';