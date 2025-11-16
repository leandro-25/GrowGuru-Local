<template>
  <ion-page class="signup-page">
    <ion-content class="h-screen overflow-hidden" :scroll-y="false">
      <div class="signup-container">
        <div class="signup-box">
          <div class="logo-wrapper">
            <img
              src="@/assets/imagem/logo.png"
              alt="GrowGuru"
            />
          </div>
          <h1 class="title">Criar Conta</h1>

          <div class="signup-form">
            <div class="form-group">
              <label>Nome Completo</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="nome"
                  type="text"
                  placeholder="Digite seu nome completo"
                ></ion-input>
              </div>
            </div>

            <div class="form-group">
              <label>Email</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="email"
                  type="email"
                  placeholder="Digite seu email"
                ></ion-input>
              </div>
            </div>

            <div class="form-group">
              <label>Senha</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="senha"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Digite sua senha"
                ></ion-input>
                <div
                  @click="showPassword = !showPassword"
                  class="toggle-password"
                >
                  <ion-icon
                    :icon="showPassword ? eyeOffOutline : eyeOutline"
                    class="w-5 h-5"
                  ></ion-icon>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Confirmar Senha</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="confirmarSenha"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="Confirme sua senha"
                ></ion-input>
                <div
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="toggle-password"
                >
                  <ion-icon
                    :icon="showConfirmPassword ? eyeOffOutline : eyeOutline"
                    class="w-5 h-5"
                  ></ion-icon>
                </div>
              </div>
            </div>

            <button
              @click="handleSignUp"
              class="submit-button"
              :disabled="loading"
            >
              <ion-spinner
                v-if="loading"
                name="crescent"
              ></ion-spinner>
              <span>{{ loading ? 'Criando conta...' : 'Criar Conta' }}</span>
            </button>

            <div class="login-container">
              <p>
                Já tem uma conta?
                <router-link to="/login" class="login-link">
                  Faça login
                </router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<style lang="scss" scoped>
@import '@/theme/singup.scss';

ion-item {
  --background: transparent;
  --border-color: transparent;
  --highlight-height: 0;
  --padding-start: 0;
  --padding-end: 0;
  --inner-padding-end: 0;
  margin-bottom: 1rem;
}

ion-item::part(native) {
  padding: 0;
  background: transparent;
}

ion-input {
  --padding-start: 1rem;
  --padding-end: 1rem;
  --padding-top: 0.75rem;
  --padding-bottom: 0.75rem;
  --placeholder-color: #9CA3AF;
  --background: rgba(31, 41, 55, 0.5);
}

ion-input.ion-focused {
  --background: rgba(31, 41, 55, 0.5);
}
</style>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { api } from '@/api';
  import { eyeOutline, eyeOffOutline } from 'ionicons/icons';
  import {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    IonText,
    IonIcon,
    toastController
  } from '@ionic/vue';
  
  // Add these refs
  const showPassword = ref(false);
  const showConfirmPassword = ref(false);
  
  const router = useRouter();
  const nome = ref('');
  const email = ref('');
  const senha = ref('');
  const confirmarSenha = ref('');
  
  const showToast = async (message, color = 'success') => {
    const toast = await toastController.create({
      message,
      duration: 3000,
      color,
      position: 'top'
    });
    await toast.present();
  };
  
  // Add loading state
  const loading = ref(false);
  
  // Update handleSignUp to use loading state
  const handleSignUp = async () => {
    try {
      loading.value = true;
      // Validação básica
      if (!nome.value || !email.value || !senha.value) {
        return showToast('Preencha todos os campos!', 'warning');
      }
  
      if (senha.value !== confirmarSenha.value) {
        return showToast('As senhas não coincidem!', 'warning');
      }
  
      const { data } = await api.post('/signup', {
        nome: nome.value.trim(),
        email: email.value.trim().toLowerCase(),
        password: senha.value
      });
  
      if (data.user) {
        await showToast('Cadastro realizado com sucesso!');
        router.push('/login');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Erro ao cadastrar';
      showToast(errorMessage, 'danger');
      console.error('Signup error:', error);
    }
  };
  </script>