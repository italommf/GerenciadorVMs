# **Gerenciador de Máquinas Virtuais**

## **1. Introdução**

### **1.1 Propósito**
Este documento descreve a visão geral do sistema **Gerenciador de Máquinas Virtuais (GMV)**, uma ferramenta para gerenciar e monitorar máquinas virtuais usadas em processos de automação RPA. O objetivo é aumentar a eficiência na execução de robôs, simplificar o controle das máquinas e reduzir significativamente o tempo de abertura e gerenciamento das VMs.

### **1.2 Escopo**
O GMV é uma solução local, projetada para rodar em máquinas com sistemas operacionais Windows 10 e 11. Ele permite que administradores e operadores possam abrir, fechar, listar e monitorar máquinas virtuais de forma centralizada. O sistema também integra ferramentas de automação como `uiautomation` e Selenium, com planos futuros de adicionar funcionalidades para controle direto dos RPAs em execução nas máquinas virtuais.

---

## **2. Descrições do Sistema**

### **2.1 Ambiente**
O GMV será executado localmente no Windows 10 e 11, utilizando uma interface desktop compatível com diferentes resoluções. A ferramenta será instalada diretamente nas máquinas físicas dos usuários, permitindo o gerenciamento eficiente das VMs e garantindo integração com ferramentas de automação já existentes.

### **2.2 Funcionalidades**
1. **Login:** Autenticação dos usuários por meio de credenciais locais.  
2. **Abrir VM:** Iniciar uma máquina virtual com as configurações armazenadas no banco de dados.  
3. **Fechar VM:** Encerrar uma máquina virtual em execução.  
4. **Monitorar Robôs:** Visualizar o status dos RPA em execução dentro das VMs.  
5. **Gerenciar Áreas de Trabalho:** Configurar múltiplas áreas de trabalho por máquina.  
6. **Listar VMs:** Exibir todas as máquinas cadastradas e seus status.  
7. **Logs e Histórico:** Exibir relatórios de uso das máquinas e status dos robôs.

**Funcionalidade Futura:** Controle direto do status e execução dos RPAs para garantir maior monitoramento e confiabilidade.

---

## **3. Atores e Casos de Uso**

### **3.1 Atores**
- **Administrador de Sistema:** Configura as VMs, gerencia permissões e realiza ajustes técnicos.  
- **Operador de RPA:** Utiliza as VMs para rodar automações.  
- **Gerente:** Acompanha relatórios e informações sobre desempenho das máquinas e robôs.  

---

### **3.2 Casos de Uso - Operador de RPA**

#### **Caso de Uso: Login**  
1. O operador acessa a tela de login.  
2. Insere suas credenciais.  
3. O sistema valida o acesso e redireciona para o painel principal.  

#### **Caso de Uso: Abrir Máquina Virtual**  
1. O operador seleciona uma VM na lista.  
2. Clica na opção "Abrir".  
3. O sistema executa a máquina com as configurações salvas.  
4. A tela da VM é exibida, reduzindo o tempo de abertura de 20 segundos (manual) para aproximadamente 2,5 segundos.  

#### **Caso de Uso: Monitorar Robôs**  
1. O operador acessa o painel de status.  
2. Seleciona uma VM para verificar os robôs em execução.  
3. O sistema exibe informações como status, logs e erros.  

---

### **3.3 Casos de Uso - Administrador de Sistema**

#### **Caso de Uso: Gerenciar VMs**  
1. O administrador acessa o painel de configurações.  
2. Cadastra ou edita as informações de uma VM, como IP, credenciais e configurações.  
3. Salva as alterações.  

#### **Caso de Uso: Gerenciar Áreas de Trabalho**  
1. O administrador seleciona uma máquina virtual.  
2. Configura múltiplas áreas de trabalho com aplicativos pré-definidos.  
3. Salva as configurações para futuros acessos.  

---

## **4. Requisitos Não Funcionais**

### **4.1 Acessibilidade**
- O sistema deve possuir uma interface simples e intuitiva para que usuários com diferentes níveis de conhecimento técnico possam utilizá-lo sem dificuldade.  
- Botões e menus devem ser autoexplicativos e organizados de forma clara.  
- Suporte a resoluções de tela variadas, garantindo boa exibição em monitores convencionais e wide.  
- Instruções e mensagens de erro devem ser exibidas de maneira compreensível, sem jargões técnicos.

### **4.2 Desempenho**
- O tempo médio para abrir uma máquina virtual deve ser de **2,5 segundos**, com limite máximo de 5 segundos em 95% dos casos.  
- O tempo para listar as VMs cadastradas deve ser inferior a **1 segundo**, independentemente da quantidade de máquinas registradas.  
- Processos intensivos, como monitoramento de robôs, devem ser realizados em background para não impactar a performance da interface.

### **4.3 Segurança**
- As credenciais das VMs devem ser armazenadas de forma criptografada no banco de dados.  
- A comunicação entre os componentes do sistema deve utilizar protocolos seguros (ex.: TLS).  
- A autenticação de usuários deve incluir validação de senha com padrões de segurança elevados.  
- Registros de atividades (logs) devem ser protegidos contra acesso não autorizado e armazenados por um período configurável.

### **4.4 Escalabilidade**
- Suporte inicial para até **50 máquinas virtuais simultâneas**.  
- Possibilidade de expansão futura para mais de **100 VMs**, com otimização do banco de dados e processos.  
- Garantia de que operações como listar VMs ou monitorar robôs sejam realizadas de forma eficiente mesmo com o aumento da carga.

### **4.5 Compatibilidade**
- Exclusivamente para Windows 10 e 11.  
- Deve funcionar em dispositivos com arquitetura de 64 bits.  
- Garantir suporte nativo às bibliotecas utilizadas, como `uiautomation` e Selenium, no ambiente Windows.  
- A interface gráfica deve se comportar corretamente tanto em monitores com resolução Full HD quanto em configurações superiores.

### **4.6 Confiabilidade**
- Disponibilidade mínima de **99,5%** em condições normais de uso.  
- Em caso de falhas, o sistema deve gerar logs detalhados para facilitar a análise e correção de erros.  
- Recuperação de operações interrompidas, como tentativa de reabrir uma VM caso ocorra erro de conexão.

### **4.7 Manutenibilidade**
- Código deve ser modular, com separação clara de responsabilidades entre os componentes.  
- Atualizações de segurança e melhorias devem ser aplicáveis sem impactar o uso atual do sistema.  
- Deve permitir que administradores ajustem configurações diretamente pelo painel ou por arquivos de configuração acessíveis.

### **4.8 Usabilidade**
- Deve incluir feedback visual para todas as ações realizadas (ex.: animação ou mensagem confirmando o sucesso ao abrir uma VM).  
- Disponibilizar atalhos de teclado para usuários avançados.  
- Layout responsivo para garantir boa experiência em diferentes tamanhos de tela.

---

## **5. Benefícios**

- Redução do tempo de abertura das máquinas virtuais de cerca de 20 segundos (manualmente) para aproximadamente 2,5 segundos.  
- Maior eficiência no gerenciamento de máquinas virtuais.  
- Redução de erros manuais durante a execução de RPA.  
- Controle centralizado de várias áreas de trabalho.  
- Melhor visibilidade do status dos robôs e das máquinas virtuais.  

---

## **6. Glossário**

- **VM:** Máquina Virtual.  
- **RPA:** Automação de Processos Robóticos.  
- **Área de Trabalho:** Espaço de execução dentro de uma VM para organizar aplicativos e processos.  
- **Logs:** Registros das atividades realizadas no sistema.  
- **Login Local:** Autenticação feita diretamente no sistema, sem necessidade de servidores externos.  

---

Pronto! Salve este conteúdo como um arquivo `.md`, e ele estará pronto para uso. Caso precise de mais ajustes, é só falar! 😊
