\c supermario;

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

-- 2. Se a vida do personagem chegar a 0, ele perde pontos

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

-- Impedir que um Personagem tenha registros tanto na tabela Jogador quanto na tabela Inimigo.

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



-- Apenas Jogador pode ter moedas ou inventário. Se um Inimigo for inserido ou atualizado, ele não pode ter esses atributos.
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


-- Quando um Personagem for deletado, garantir que ele seja removido automaticamente das tabelas Jogador e Inimigo.

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

-- Trigger para atualizar a posição do jogador no checkpoint
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

-- Trigger para garantir que personagens não sejam criados sem vida mínima
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

-- Trigger para atualizar a quantidade de moedas do jogador

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