<template>
  <ion-modal 
    :is-open="isOpen" 
    @didDismiss="closeModal" 
    class="transactions-modal"
    :backdrop-dismiss="true"
    :can-dismiss="true"
  >
    <!-- O cabeçalho agora é um elemento de nível superior para ficar fixo -->
    <div class="modal-header">
      <h2 class="modal-title">Minhas Transações</h2>
      <button class="close-button" @click="closeModal">
        <ion-icon :icon="closeOutline"></ion-icon>
      </button>
    </div>

    <!-- O ion-content cuidará da área de rolagem -->
    <ion-content class="transactions-content">
      <div class="transactions-list-container">
        <!-- Estado de Carregamento (Bônus, opcional) -->
        <!-- <div v-if="loading">Carregando...</div> -->

        <!-- Estado Vazio -->
        <div v-if="!transactions || transactions.length === 0" class="empty-state">
          <ion-icon :icon="receiptOutline" class="empty-icon"></ion-icon>
          <p>Nenhuma transação encontrada</p>
        </div>
        
        <!-- Lista de Transações -->
        <template v-else>
          <transition-group name="fade-list" tag="div">
            <div 
              v-for="transacao in transactions" 
              :key="transacao.id" 
              class="transaction-item"
            >
              <div class="transaction-info">
                  <ion-icon 
                    :icon="transacao.tipo.toLowerCase() === 'venda' ? arrowBackCircleOutline : arrowForwardCircleOutline" 
                    class="transaction-icon"
                  ></ion-icon>
                  <div class="transaction-text">
                    <div class="transaction-header">
                      <h4 class="transaction-type">
                        {{ transacao.tipo }}
                        <span :class="['transaction-amount', transacao.tipo.toLowerCase() === 'venda' ? 'income' : 'expense']">
                          {{ formatCurrency(transacao.valor) }}
                        </span>
                      </h4>
                    </div>
                    <p class="transaction-description">
                      {{ transacao.descricao || 'Compra de 1 cotas' }}
                    </p>
                    <p class="transaction-date">
                      <ion-icon :icon="timeOutline" class="date-icon"></ion-icon>
                      {{ formatDate(transacao.data) }}
                    </p>
                  </div>
                </div>
            </div>
          </transition-group>
        </template>
      </div>
    </ion-content>
  </ion-modal>
</template>

<script>
import { 
  IonModal, 
  IonContent,
  IonIcon
} from '@ionic/vue';
import { 
  closeOutline, 
  arrowBackCircleOutline, 
  arrowForwardCircleOutline,
  receiptOutline,
  timeOutline
} from 'ionicons/icons';

export default {
  name: 'TransactionsModal',
  components: {
    IonModal,
    IonContent,
    IonIcon
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    transactions: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  watch: {
    transactions: {
      handler(newVal) {
        console.log('Transações recebadas no modal:', newVal);
      },
      immediate: true,
      deep: true
    }
  },
  setup() {
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        // Retorna um placeholder ou a data original se for inválida
        return 'Data inválida';
      }
      const options = { 
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
      };
      return date.toLocaleDateString('pt-BR', options).replace(',', ' às');
    };

    const formatCurrency = (value) => {
      if (typeof value !== 'number') return 'R$ 0,00';
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value);
    };

    return {
      closeOutline,
      arrowBackCircleOutline,
      arrowForwardCircleOutline,
      receiptOutline,
      timeOutline,
      formatDate,
      formatCurrency
    };
  },
  methods: {
    closeModal() {
      this.$emit('update:isOpen', false);
    }
  }
};
</script>

<style lang="scss">
  // Importamos o SCSS externo do tema
  // IMPORTANTE: Não use 'scoped' para que os estilos de ::part funcionem
  @import '../theme/TransactionsModal.scss';
</style>