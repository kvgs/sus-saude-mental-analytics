-- ================================================
-- Análise de Internações Psiquiátricas no SUS - SP
-- Fonte: DATASUS / SIH (2017-2023)
-- ================================================

-- 1. Total de internações por ano e período
SELECT
    ANO,
    PERIODO,
    COUNT(*) AS total_internacoes,
    ROUND(AVG(DIAS_PERM), 1) AS media_dias,
    ROUND(AVG(VAL_TOT), 2) AS media_valor
FROM internacoes
GROUP BY ANO, PERIODO
ORDER BY ANO;

-- 2. Ranking de diagnósticos por volume
SELECT
    GRUPO_DIAG,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct_total,
    ROUND(AVG(DIAS_PERM), 1) AS media_dias,
    ROUND(AVG(VAL_TOT), 2) AS media_valor
FROM internacoes
GROUP BY GRUPO_DIAG
ORDER BY total DESC;

-- 3. Internações por sexo e diagnóstico
SELECT
    GRUPO_DIAG,
    SEXO,
    COUNT(*) AS total,
    ROUND(AVG(DIAS_PERM), 1) AS media_dias,
    ROUND(MEDIAN(DIAS_PERM), 1) AS mediana_dias
FROM internacoes
GROUP BY GRUPO_DIAG, SEXO
ORDER BY GRUPO_DIAG, SEXO;

-- 4. Impacto da pandemia por diagnóstico
-- (média anual normalizada por período)
SELECT
    GRUPO_DIAG,
    PERIODO,
    COUNT(*) AS total,
    ROUND(COUNT(*) / CASE
        WHEN PERIODO = 'Pré-pandemia' THEN 3.0
        WHEN PERIODO = 'Pandemia'     THEN 2.0
        WHEN PERIODO = 'Pós-pandemia' THEN 2.0
    END, 0) AS media_anual
FROM internacoes
GROUP BY GRUPO_DIAG, PERIODO
ORDER BY GRUPO_DIAG, PERIODO;

-- 5. Taxa de óbito por diagnóstico e período
SELECT
    GRUPO_DIAG,
    PERIODO,
    COUNT(*) AS total_internacoes,
    SUM(MORTE) AS total_obitos,
    ROUND(AVG(MORTE) * 100, 3) AS taxa_obito_pct
FROM internacoes
GROUP BY GRUPO_DIAG, PERIODO
ORDER BY taxa_obito_pct DESC;

-- 6. Sazonalidade — média de internações por mês
SELECT
    strftime('%m', DT_INTER) AS mes,
    CASE strftime('%m', DT_INTER)
        WHEN '01' THEN 'Janeiro'
        WHEN '02' THEN 'Fevereiro'
        WHEN '03' THEN 'Março'
        WHEN '04' THEN 'Abril'
        WHEN '05' THEN 'Maio'
        WHEN '06' THEN 'Junho'
        WHEN '07' THEN 'Julho'
        WHEN '08' THEN 'Agosto'
        WHEN '09' THEN 'Setembro'
        WHEN '10' THEN 'Outubro'
        WHEN '11' THEN 'Novembro'
        WHEN '12' THEN 'Dezembro'
    END AS nome_mes,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 1.0 / 7, 0) AS media_anual
FROM internacoes
GROUP BY mes
ORDER BY mes;

-- 7. Perfil por raça/cor e diagnóstico
SELECT
    RACA_COR,
    GRUPO_DIAG,
    COUNT(*) AS total,
    ROUND(AVG(DIAS_PERM), 1) AS media_dias
FROM internacoes
WHERE RACA_COR != 'Ignorado'
GROUP BY RACA_COR, GRUPO_DIAG
ORDER BY RACA_COR, total DESC;