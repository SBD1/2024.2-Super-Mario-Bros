## Introdução

Triggers e Stored Procedures são mecanismos do banco de dados utilizados para automação e integridade dos dados. Triggers são gatilhos que executam ações automaticamente em resposta a eventos como inserções, atualizações ou exclusões em uma tabela, sendo úteis para auditoria, manutenção da integridade referencial e implementação de regras de negócio. Já Stored Procedures são conjuntos de comandos SQL armazenados no banco, que podem ser executados sob demanda para realizar operações complexas, otimizando o desempenho e reduzindo a redundância no código. Ambos contribuem para a segurança, eficiência e organização da lógica de negócios no banco de dados.

# Triggers

??? "Trigger: atualizar_vida"

    ```sql
    -- Função que será chamada pelo trigger
    CREATE OR REPLACE FUNCTION atualizar_vida() RETURNS TRIGGER AS $$ 
    BEGIN
    -- A vida máxima será o nível multiplicado por 100
    IF NEW.vida > (NEW.nivel * 100) THEN
        NEW.vida := (NEW.nivel * 100);  -- Limita a vida ao valor máximo
    END IF;

    -- Se a vida for menor que o mínimo, ajusta para 0
    IF NEW.vida < 0 THEN
        NEW.vida := 0;  -- A vida não pode ser negativa
    END IF;

    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_atualizar_vida
    BEFORE UPDATE ON personagem
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_vida();
    ```