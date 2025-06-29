-- Consolidar materiais duplicados por nome normalizado
CREATE TEMP TABLE temp_materiais_consolidados AS
SELECT
  LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
    nome,
    'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u'),'ã','a'),'õ','o'),'â','a'),'ê','e'),'ô','o')) AS nome_normalizado,
  MAX(id) as id_principal,
  SUM(quantidade_disponivel) as quantidade_total,
  MAX(estoque_minimo) as estoque_minimo,
  MAX(valor_unitario) as valor_unitario,
  MAX(unidade) as unidade,
  MAX(descricao) as descricao
FROM materiais
WHERE ativo = 1
GROUP BY nome_normalizado;

UPDATE materiais
SET quantidade_disponivel = (
  SELECT quantidade_total
  FROM temp_materiais_consolidados t
  WHERE t.id_principal = materiais.id
)
WHERE id IN (SELECT id_principal FROM temp_materiais_consolidados);

UPDATE materiais
SET ativo = 0
WHERE id NOT IN (SELECT id_principal FROM temp_materiais_consolidados)
  AND LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
    nome,
    'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u'),'ã','a'),'õ','o'),'â','a'),'ê','e'),'ô','o')) IN (
    SELECT nome_normalizado FROM temp_materiais_consolidados
  )
  AND ativo = 1;

DROP TABLE temp_materiais_consolidados; 