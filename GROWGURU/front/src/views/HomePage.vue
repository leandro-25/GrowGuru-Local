<template>
  <ion-page class="home-page">
    <ion-content 
      ref="content" 
      class="ion-padding" 
      :scroll-events="true" 
      @ionRefresh="handleRefresh($event)" 
      :fullscreen="true"
    >
      <!-- Meta viewport para melhor responsividade -->
      <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, maximum-scale=1.0, user-scalable=no">
      <ion-refresher slot="fixed" @ionRefresh="handleRefresh($event)">
        <ion-refresher-content pulling-icon="chevron-down-circle-outline"
          refreshing-spinner="circles"></ion-refresher-content>
      </ion-refresher>

      <div v-if="isLoading" class="loading-indicator">
        <ion-spinner></ion-spinner>
        <p>Carregando...</p>
      </div>

      <div class="content-container" :class="{ 'content-loading': isLoading }">
        <div class="brand-container">
          <div class="logo-container">
            <img src="@/assets/imagem/logoP.png" alt="Logo" class="logo-image">
            <div class="brand-text">
              <span class="brand-bold">Grow</span>Guru
            </div>
          </div>
          <button @click="openProfileMenu" class="profile-button-top">
            <ion-icon :icon="personOutline" class="profile-icon"></ion-icon>
          </button>

          <!-- Menu de botões flutuantes -->
          <div v-if="profileMenuOpen" class="floating-menu">
            <div class="floating-menu-backdrop" @click="profileMenuOpen = false"></div>
            <div class="floating-menu-buttons">
              <button class="floating-menu-button" @click="goToProfile">
                <ion-icon :icon="personOutline" class="menu-icon"></ion-icon>
                <span>Meu Perfil</span>
              </button>
              <button class="floating-menu-button logout-button" @click="logout">
                <ion-icon :icon="logOutOutline" class="menu-icon"></ion-icon>
                <span>Sair</span>
              </button>
            </div>
          </div>
        </div>

        <div class="balance-card">
          <div class="card-content">
            <div class="user-info">
              <h2 class="user-name">Olá {{ userName }}</h2>
              <p class="account-date">Conta desde {{ formatDateShort(userCreatedAt) }}</p>
            </div>
            <div class="balance-info">
              <div class="balance-row">
                <div class="balance-item">
                  <p class="balance-label">Rentabilidade</p>
                  <p
                    :class="['balance-value', (saldo < 0 && totalInvestido === 0) ? 'loss' : (totalInvestido === 0 ? 'neutral' : (saldo + totalInvestido) >= 0 ? 'profit' : 'loss')]">
                    {{ (totalInvestido === 0 && saldo < 0) ? `-${Math.abs(saldo).toFixed(2)}` : (totalInvestido === 0
                      ? '0.00' : `${(saldo + totalInvestido) >= 0 ? '+' : ''}${((saldo + totalInvestido) / totalInvestido
                        * 100).toFixed(2)}`) }}%
                  </p>
                </div>
                <div class="balance-item">
                  <p class="balance-label">Total investido</p>
                  <p class="balance-value">R$ {{ totalInvestido.toFixed(2) }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="card-decoration"></div>
          <img src="@/assets/imagem/visa.png" alt="Visa Logo" class="card-logo" />
        </div>

        <div class="transactions-section">
          <div class="section-header">
            <h3 class="section-title">Transações recentes</h3>
            <button class="see-more" @click="openTransactionsModal">Ver mais</button>
          </div>
          <div class="transactions-list">
            <div v-if="visibleTransactions.length === 0" class="empty-state">
              <p>Nenhuma transação encontrada</p>
            </div>
            <div v-for="transacao in visibleTransactions" :key="transacao.id" class="transaction-item">
              <div class="transaction-info">
                <ion-icon :icon="transacao.tipo.toLowerCase() === 'venda' ? arrowBackCircleOutline : arrowForwardCircleOutline" 
                        color="warning" class="transaction-icon"
                        style="font-size: 32px; width: 32px; height: 32px; --ionicon-stroke-width: 32px;">
                </ion-icon>
                <div class="transaction-text">
                  <h4 class="transaction-type">
                    {{ transacao.tipo }}
                  </h4>
                  <p class="transaction-description">
                    {{ transacao.descricao }}
                  </p>
                  <p class="transaction-date">{{ formatDate(transacao.data) }}</p>
                </div>
              </div>
              <span :class="['transaction-amount', transacao.tipo.toLowerCase() === 'venda' ? 'income' : 'expense']">
                R$ {{ transacao.valor.toFixed(2) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Botão Flutuante (FAB) removido conforme solicitado -->
      
      <!-- Adicionando um rodapé para melhorar a experiência em dispositivos com notch -->
      <div class="safe-area-spacer"></div>
    </ion-content>
    <!-- Modal de Transações -->
    <TransactionsModal 
      :isOpen="isTransactionsModalOpen"
      :transactions="allTransactions"
      @update:isOpen="isTransactionsModalOpen = $event"
    />
  </ion-page>
</template>

<script setup>
import { ref, computed, onMounted, onActivated, onUnmounted, nextTick, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { api } from '@/api';
// Importar componentes
import TransactionsModal from '@/views/TransactionsModal.vue';
import { 
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonSpinner,
  IonRefresher,
  IonRefresherContent,
  IonIcon,
  IonPopover,
  IonList,
  IonItem,
  IonLabel,
  toastController
} from '@ionic/vue';
import { 
  addCircle, 
  walletOutline, 
  logOutOutline, 
  personCircleOutline,
  refreshOutline,
  chevronDownOutline,
  chevronUpOutline,
  addOutline,
  removeOutline,
  arrowForwardCircleOutline,
  arrowBackCircleOutline,
  personOutline
} from 'ionicons/icons';

const router = useRouter();
const content = ref(null);

// Estados de controle
const isLoading = ref(false);
const lastUpdate = ref(null);
const isTransactionsModalOpen = ref(false);

// Função de navegação removida junto com o botão FAB
/* Estados do menu de perfil */
const profileMenuOpen = ref(false);
const popoverEvent = ref(null);

// Dados do usuário
const userName = ref('Usuário');
const saldo = ref(0);
const totalInvestido = ref(0);
const userCreatedAt = ref('');

// Dados das transações
const allTransactions = ref([]);
const currentPage = ref(1);
const limit = 4;
const windowStart = ref(0);

const visibleTransactions = computed(() => {
  return allTransactions.value.slice(windowStart.value, windowStart.value + limit);
});

const formatDate = (dataISO) => {
  return new Date(dataISO).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const formatDateShort = (dataISO) => {
  return new Date(dataISO).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
};

// Função para carregar o total investido
const carregarTotalInvestido = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) return;

    // Buscar a carteira do usuário
    const { data: carteira } = await api.get('/carteira', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    });

    // Calcular o total investido somando o total_investido de cada estratégia
    const total = carteira.reduce((soma, estrategia) => {
      return soma + (parseFloat(estrategia.total_investido) || 0);
    }, 0);

    totalInvestido.value = total;
    console.log('Total investido calculado:', totalInvestido.value);
  } catch (error) {
    console.error('Erro ao carregar total investido:', error);
    totalInvestido.value = 0;
  }
};

// Função para carregar os dados do usuário
const loadUserData = async () => {
  try {
    console.log('Carregando dados do usuário...');
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Adiciona timestamp para evitar cache
    const timestamp = new Date().getTime();
    const [{ data: usuario }, _] = await Promise.all([
      api.get(`/usuarios?_t=${timestamp}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        }
      }),
      carregarTotalInvestido() // Carrega o total investido em paralelo
    ]);

    // Atualiza os dados do usuário
    userName.value = usuario.nome || 'Usuário';
    saldo.value = parseFloat(usuario.saldo) || 0;
    userCreatedAt.value = usuario.created_at;

    console.log('Dados do usuário atualizados:', {
      nome: userName.value,
      saldo: saldo.value,
      totalInvestido: totalInvestido.value
    });
    return usuario;
  } catch (error) {
    console.error('Erro ao carregar dados do usuário:', error);
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
    throw error;
  }
};

const loadInitialData = async () => {
  try {
    // Verifica se já está carregando para evitar múltiplas requisições
    if (isLoading.value) return;

    isLoading.value = true;

    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Carrega os dados do usuário
    const [usuarioResponse, transacoesResponse] = await Promise.all([
      api.get('/usuarios', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('/transacoes', {
        headers: { Authorization: `Bearer ${token}` },
        params: { page: 1, limit }
      })
    ]);

    // Atualiza os dados do usuário
    const usuario = usuarioResponse.data;
    const transacoesData = transacoesResponse.data;

    userName.value = usuario.nome || 'Usuário';
    saldo.value = parseFloat(usuario.saldo) || 0;
    userCreatedAt.value = usuario.created_at;

    // Atualiza as transações
    allTransactions.value = Array.isArray(transacoesData)
      ? transacoesData.sort((a, b) => new Date(b.data) - new Date(a.data))
      : [];

    // Atualiza o timestamp da última atualização
    lastUpdate.value = new Date();

  } catch (error) {
    console.error('Erro ao carregar dados:', error);
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
  } finally {
    isLoading.value = false;
  }
};

const loadTransactions = async (page) => {
  try {
    console.log(`Carregando transações, página ${page}...`);
    isLoading.value = true;

    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Adiciona timestamp para evitar cache
    const timestamp = new Date().getTime();
    const { data: transacoesData } = await api.get('/transacoes', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      },
      params: {
        page,
        limit,
        _t: timestamp
      }
    });

    // Se for a primeira página, substitui todas as transações
    if (page === 0) {
      allTransactions.value = [];
    }

    // Adiciona as novas transações
    transacoesData.forEach(tx => {
      if (!allTransactions.value.some(existing => existing.id === tx.id)) {
        allTransactions.value.push(tx);
      }
    });

    // Ordena por data mais recente primeiro
    allTransactions.value.sort((a, b) => new Date(b.data) - new Date(a.data));

    console.log(`Total de transações carregadas: ${allTransactions.value.length}`);
    return transacoesData;
  } catch (error) {
    console.error('Erro ao carregar transações:', error);
  } finally {
    isLoading.value = false;
  }
};

// Função para forçar atualização dos dados
const refreshData = async (event = null) => {
  try {
    await loadInitialData();
  } finally {
    if (event?.target) {
      event.target.complete();
    }
  }
};

// Configura o scroll infinito
const handleScroll = async (event) => {
  const scrollElement = event.target;
  const scrollTop = scrollElement.scrollTop;
  const scrollHeight = scrollElement.scrollHeight;
  const height = scrollElement.clientHeight;
  const scrollThreshold = 50; // pixels da parte inferior para começar a carregar mais

  // Verifica se está próximo ao final
  if (scrollHeight - (scrollTop + height) < scrollThreshold) {
    const nextPage = currentPage.value + 1;
    await loadTransactions(nextPage);
    currentPage.value = nextPage;
  }

  // Verifica se está no topo para carregar itens anteriores
  if (scrollTop <= 100 && windowStart.value > 0) {
    windowStart.value -= 1;
  }
};

// Configura o refresh ao puxar para baixo
const handleRefresh = async (event) => {
  console.log('Atualização manual acionada');
  // Reseta os estados para forçar recarregamento completo
  allTransactions.value = [];
  windowStart.value = 0;
  currentPage.value = 0;

  await refreshData(event);
};

// Função para forçar a atualização dos dados
const atualizarDados = async () => {
  try {
    console.log('Forçando atualização dos dados...');
    // Limpa os dados atuais
    allTransactions.value = [];

    // Carrega os dados do usuário
    await loadUserData();

    // Carrega as transações mais recentes
    await loadTransactions(0, true);

    console.log('Dados atualizados com sucesso!');
  } catch (error) {
    console.error('Erro ao atualizar dados:', error);
  }
};

// Função para carregar TODOS os dados
const carregarTudo = async () => {
  try {
    console.log('Iniciando carregamento de todos os dados...');

    // Carrega os dados em sequência
    await Promise.all([
      loadUserData(),
      loadTransactions(0)
    ]);

    console.log('Todos os dados foram carregados com sucesso!');
  } catch (error) {
    console.error('Erro ao carregar dados:', error);
  }
};

// Função para abrir o menu de perfil
const openProfileMenu = (event) => {
  popoverEvent.value = event;
  profileMenuOpen.value = true;
};

// Função para navegar para a página de perfil
const goToProfile = () => {
  profileMenuOpen.value = false;
  router.push('/profile');
};

// Função para fazer logout
const logout = async () => {
  try {
    profileMenuOpen.value = false;

    // Remove o token do localStorage
    localStorage.removeItem('token');

    // Mostra mensagem de sucesso
    const toast = await toastController.create({
      message: 'Desconectado com sucesso!',
      duration: 2000,
      color: 'success',
      position: 'top'
    });
    await toast.present();

    // Redireciona para a página de login
    setTimeout(() => {
      router.push('/login');
    }, 500);

  } catch (error) {
    console.error('Erro ao fazer logout:', error);
  }
};

// Função para atualizar o saldo quando receber o evento
const handleSaldoAtualizado = (event) => {
  console.log('Evento de saldo atualizado recebido:', event.detail);
  saldo.value = event.detail.novo_saldo;
  // Recarrega as transações e o total investido para garantir que tudo esteja atualizado
  loadTransactions(1);
  carregarTotalInvestido();
};

// Função para lidar com a atualização do total investido
const handleTotalInvestidoAtualizado = async () => {
  await carregarTotalInvestido();
};

// Função para abrir o modal de transações
const openTransactionsModal = async () => {
  try {
    // Se ainda não carregou todas as transações, carrega agora
    if (allTransactions.value.length <= visibleTransactions.value.length) {
      await loadTransactions(1, true);
    }
    isTransactionsModalOpen.value = true;
  } catch (error) {
    console.error('Erro ao abrir o modal de transações:', error);
  }
};

// Carrega os dados quando o componente é montado
onMounted(() => {
  console.log('Componente Home montado - Carregando dados...');
  carregarTudo();

  // Configura o listener de scroll
  nextTick(() => {
    if (content.value?.$el) {
      content.value.$el.addEventListener('scroll', handleScroll);
    }
  });

  // Adiciona o listener para o evento de atualização de saldo
  window.addEventListener('saldo-atualizado', handleSaldoAtualizado);
});

// Atualiza os dados sempre que a rota for ativada
onActivated(() => {
  console.log('Página Home ativada - Forçando atualização dos dados...');
  // Força o recarregamento completo
  carregarTudo();
});

// Atualiza os dados quando a rota for alterada (incluindo quando volta para a mesma rota)
const route = useRoute();
watch(() => route.path, (newPath, oldPath) => {
  if (newPath === '/tabs/home') {
    console.log('Rota Home detectada - Atualizando dados...');
    carregarTudo();
  }
});

onUnmounted(() => {
  if (content.value && content.value.$el) {
    content.value.$el.removeEventListener('scroll', handleScroll);
  }
});
</script>

<style lang="scss">
@use '@/theme/homepage';
</style>
