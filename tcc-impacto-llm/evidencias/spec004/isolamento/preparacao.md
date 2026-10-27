# Preparação de isolamento — capacidade não disponibilizada

27/10/2026, T014/T015 **pendentes**. A conferência de ambiente ocorreu antes da implementação, em ambiente.json, sem alteração de contas ou ACLs.

O token observado é CodexSandboxOffline, autenticado e não elevado. Esse token consegue ler a referência candidata e o desenvolvimento. A sessão não disponibilizou runner sob outra identidade com raízes/permissões que neguem leitura de desenvolvimento/referência/avaliação. A mera disponibilidade dos cmdlets Get-LocalUser/New-LocalUser/Start-Process não oferece identidade/credencial/runner já provisionado para cumprir esse contrato; não foram usados para contornar a restrição.

Capacidade exigida ainda ausente: lançar o montador com leitura somente do runner/pacote permitido e escrita somente em saída nova, sob identidade cuja leitura das zonas proibidas seja efetivamente negada. É necessária configuração operacional externa/autorizada e prova posterior, preservando sentinelas fictícias e comandos/retornos. Não houve tentativa de criar conta, modificar ACL, obter credencial ou elevar privilégios para essa prova.

Os controles de path produziram provas reais de recusa de junctions internas/externas. A criação de symlink real foi negada com WinError1314 (stderr original em montagem-final); o método permanece ignorado, sem escalar para ultrapassar a capacidade ausente. O teste controlado do bit reparse é somente lógica de validação; não é prova de isolamento de identidade.

Resultado: separação lógica implementada; isolamento efetivo não demonstrado. Nenhum arquivo de gabarito foi copiado para os pacotes. Sem liberação de envio/piloto ou fechamento integral.
