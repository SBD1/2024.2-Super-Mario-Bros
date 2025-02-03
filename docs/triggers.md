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

??? "Trigger: after_update_vida_personagem"

    ```sql
    -- Função que será chamada pelo trigger
    CREATE OR REPLACE FUNCTION after_update_vida_personagem() RETURNS TRIGGER AS $$ 
    BEGIN
    IF NEW.vida <= 0 THEN
        UPDATE personagem 
        SET pontos = GREATEST(0, pontos - 10) 
        WHERE idPersonagem = NEW.idPersonagem;
    END IF;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_after_update_vida_personagem
    AFTER UPDATE ON personagem
    FOR EACH ROW
    EXECUTE FUNCTION after_update_vida_personagem();

    ```

??? "Trigger: verificar_unicidade_personagem"

    ```sql
    -- Função que será chamada pelo trigger
    CREATE OR REPLACE FUNCTION verificar_unicidade_personagem() RETURNS TRIGGER AS $$ 
    BEGIN
    IF (SELECT COUNT(*) FROM Jogador WHERE idPersonagem = NEW.idPersonagem) > 0 AND
       (SELECT COUNT(*) FROM Inimigo WHERE idPersonagem = NEW.idPersonagem) > 0 THEN
        RAISE EXCEPTION 'Um personagem não pode ser Jogador e Inimigo ao mesmo tempo!';
    END IF;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_verificar_unicidade_jogador
    BEFORE INSERT OR UPDATE ON Jogador
    FOR EACH ROW
    EXECUTE FUNCTION verificar_unicidade_personagem();

    CREATE TRIGGER trg_verificar_unicidade_inimigo
    BEFORE INSERT OR UPDATE ON Inimigo
    FOR EACH ROW
    EXECUTE FUNCTION verificar_unicidade_personagem();

    ```

??? "Trigger: impedir_moeda_inventario_para_inimigos"

    ```sql
    CREATE OR REPLACE FUNCTION impedir_moeda_inventario_para_inimigos() RETURNS TRIGGER AS $$ 
    BEGIN
    IF EXISTS (SELECT 1 FROM Inimigo WHERE idPersonagem = NEW.idPersonagem) THEN
        IF NEW.moeda IS NOT NULL OR NEW.idInventario IS NOT NULL THEN
            RAISE EXCEPTION 'Inimigos não podem ter moedas ou inventário!';
        END IF;
    END IF;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_impedir_moeda_inventario_inimigo
    BEFORE INSERT OR UPDATE ON Jogador
    FOR EACH ROW
    EXECUTE FUNCTION impedir_moeda_inventario_para_inimigos();

    ```

??? "Trigger: remover_jogador_ou_inimigo_ao_excluir_personagem"

    ```sql
    CREATE OR REPLACE FUNCTION remover_jogador_ou_inimigo_ao_excluir_personagem()
    RETURNS TRIGGER AS $$
    BEGIN
    DELETE FROM Jogador WHERE idPersonagem = OLD.idPersonagem;
    DELETE FROM Inimigo WHERE idPersonagem = OLD.idPersonagem;
    RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_remover_jogador_ou_inimigo_ao_excluir_personagem
    AFTER DELETE ON Personagem
    FOR EACH ROW
    EXECUTE FUNCTION remover_jogador_ou_inimigo_ao_excluir_personagem();


    ```

??? "Trigger: atualizar_posicao_checkpoint"

    ```sql
    CREATE OR REPLACE FUNCTION atualizar_posicao_checkpoint() RETURNS TRIGGER AS $$ 
    BEGIN
    UPDATE jogador
    SET idLocal = NEW.idLocal
    WHERE idPersonagem = NEW.idPersonagem;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_atualizar_posicao_checkpoint
    AFTER INSERT ON checkpoint
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_posicao_checkpoint();


    ```

??? "Trigger: garantir_vida_minima"

    ```sql
    CREATE OR REPLACE FUNCTION garantir_vida_minima() RETURNS TRIGGER AS $$ 
    BEGIN
    IF NEW.vida < 1 THEN
        NEW.vida := 1;
    END IF;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_garantir_vida_minima
    BEFORE INSERT ON personagem
    FOR EACH ROW
    EXECUTE FUNCTION garantir_vida_minima();


    ```

??? "Trigger: atualizar_moedas_jogador"

    ```sql
    CREATE OR REPLACE FUNCTION atualizar_moedas_jogador() RETURNS TRIGGER AS $$ 
    BEGIN
    UPDATE jogador
    SET moeda = moeda + NEW.valor
    WHERE idPersonagem = NEW.idPersonagem;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trg_atualizar_moedas_jogador
    AFTER INSERT ON jogador
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_moedas_jogador();


    ```

