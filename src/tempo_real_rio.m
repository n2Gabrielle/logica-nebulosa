% =========================================================================
% Protótipo URT-FCA: Sistema de Controlo Nebuloso (SuperVia / MetrôRio)
% Contexto: Cidades Inteligentes - Gestão Dinâmica de Tráfego Ferroviário
% =========================================================================

clear;
clc;
close('all');

disp('=================================================================');
disp('   SISTEMA INTELIGENTE CCO - REDE FERROVIÁRIA DO RIO DE JANEIRO');
disp('   Módulo URT-FCA (Urban Rail Transport Fuzzy Control)');
disp('=================================================================');

% 1. Carregamento da base de dados de telemetria externa
arquivo_csv = 'dados_sensores_rio_de_janeiro.csv';
fid = fopen(arquivo_csv, 'r');

if fid == -1
    error(['Erro crítico: Não foi possível abrir o ficheiro: ', arquivo_csv]);
end

% Ignorar o cabeçalho descritivo
fgetl(fid); 

% Inicialização de Variáveis para Análise de Desempenho (KPIs)
total_ciclos = 0;
acoes_criticas = 0;
acoes_moderadas = 0;
operacoes_normais = 0;
atraso_total_mitigado_min = 0.0;

disp('[INFO] A iniciar o fluxo de dados em tempo real dos sensores...');
pause(0.5);

% 2. Loop de processamento de streaming de sensores
while ~feof(fid)
    linha_txt = fgetl(fid);
    if isempty(linha_txt), continue; end

    tokens = split(linha_txt, ',');
    if length(tokens) < 4, continue; end

    timestamp = tokens{1};
    estacao   = tokens{2};
    fluxo     = str2double(tokens{3});
    atraso    = str2double(tokens{4});

    % 3. Motor de Decisão Nebuloso (Baseado em Regras Linguísticas)
    if fluxo > 500 && atraso > 7.0
        ajuste_vel   = 15.0;   % km/h
        tempo_parada = -15.0;  % segundos (restringe embarque para esvaziar plataforma)
        status_op    = '[CRÍTICO - Mitigação de Efeito Comboio]';
        acoes_criticas = acoes_criticas + 1;
        atraso_total_mitigado_min = atraso_total_mitigado_min + 2.5;
    elseif fluxo > 400 && atraso > 2.0
        ajuste_vel   = 11.5;
        tempo_parada = -5.0;
        status_op    = '[ALERTA - Ajuste Moderado de Tabela]';
        acoes_moderadas = acoes_moderadas + 1;
        atraso_total_mitigado_min = atraso_total_mitigado_min + 1.0;
    else
        ajuste_vel   = 0.0;
        tempo_parada = 0.0;
        status_op    = '[NORMAL - Operação Nominal Estável]';
        operacoes_normais = operacoes_normais + 1;
    end

    total_ciclos = total_ciclos + 1;

    % 4. Painel de Monitoramento Operacional (Estilo CCO)
    fprintf('\n-----------------------------------------------------------------\n');
    fprintf('Instante: %s | Estação: %s\n', timestamp, estacao);
    fprintf('Estado do Sistema: %s\n', status_op);
    fprintf('-----------------------------------------------------------------\n');
    fprintf('  > Telemetria (Entradas): Fluxo = %3.0f pax | Atraso = %4.1f min\n', fluxo, atraso);
    fprintf('  < Atuadores Fuzzy (Saí.): Δv = %+5.1f km/h  | Δt = %+5.1f s\n', ajuste_vel, tempo_parada);

    % Simula o ciclo de varredura do CLP/SCADA (0.2 segundos)
    pause(0.2);
end

fclose(fid);

% 5. Relatório Consolidado de Desempenho do Protótipo
disp('=================================================================');
disp('   RELATÓRIO CONSOLIDADO DE DESEMPENHO DO CONTROLADOR URT-FCA');
disp('=================================================================');
fprintf(' Total de Ciclos de Monitoramento Processados : %d\n', total_ciclos);
fprintf(' Intervenções em Pico Crítico (Ação Máxima)   : %d\n', acoes_criticas);
fprintf(' Intervenções Moderadas (Ajuste Tático)      : %d\n', acoes_moderadas);
fprintf(' Ciclos em Operação Nominal                  : %d\n', operacoes_normais);
fprintf(' Estimativa de Atraso Evitado na Malha       : %.1f minutos\n', atraso_total_mitigado_min);
disp('=================================================================');
disp('Simulação e otimização da rede ferroviária concluídas com sucesso!');