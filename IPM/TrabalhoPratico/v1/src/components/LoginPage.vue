<template>
    <div class="login-page">
      <div class="left-side">
        <div class="logo">
          <h1>MinhoSync</h1>
          <p class="slogan">O teu horário, sincronizado ao teu ritmo!</p>
        </div>
        <p class="quote">"O saber começa com o conhecimento do tempo próprio." - Sócrates</p>
      </div>
      <div class="right-side">
        <div class="login-container">
          <h2>Entre na sua conta</h2>
          <p>Faça a sua autenticação para entrar no sistema</p>
          <form @submit.prevent="login">
            <input 
              type="email" 
              v-model="email" 
              placeholder="Email" 
              required 
            />
            <input 
              type="password" 
              v-model="password" 
              placeholder="Password" 
              required 
            />
            <button type="submit">Entrar no sistema</button>
          </form>
          <p class="or-text">Ou entrar com</p>
          <button class="minho-auth" @click="loginUMinho">Autenticação UMinho</button>
          <p>Não tens conta? <a href="/register">Registra-te</a></p> 
          <p>Todos os direitos reservados © MinhoSync</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: {
      login() {
        // Lógica de login
        console.log('A tentar fazer login com', this.email, this.password);
      },
      loginUMinho() {
        // Lógica para autenticação UMinho
        console.log('Autenticação UMinho');
      }
    }
  };
  </script>
  
  <style scoped>
  /* Layout da página dividida ao meio */
  .login-page {
    display: flex;
    flex-direction: row; /* Divisão vertical */
    height: 100vh;
  }
  
  .left-side {
    background-color: #b21b2d; /* Vermelho */
    color: white;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px;
  }
  
  .right-side {
    background-color: white;
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  h1 {
    font-size: 3em; /* Tamanho maior para o título */
    margin-bottom: 0.5em;
    font-family: 'Montserrat'; /* Fonte Montserrat para MinhoSync */
  }
  
  .slogan {
    font-size: 1.5em;
    font-family: 'Inter',bold; /* Fonte Inter para o slogan */
  }
  
  .quote {
    font-size: 0.8em;
    color: rgb(181, 181, 181);
    text-align: left;
    margin-top: auto;
    font-family: 'Fenix', serif; /* Fonte Fenix para a frase de Sócrates */
  }
  
  input {
    width: 100%; /* Garante que o campo de entrada ocupe 100% da largura disponível */
    padding: 0.8em;
    margin-bottom: 1em;
    border-radius: 5px;
    border: 1px solid #ccc;
    font-size: 1em;
  }
  
  button {
    background-color: #b21b2d;
    color: white;
    padding: 0.8em;
    border: none;
    width: 108%; /* Garante que o botão ocupe 100% da largura disponível */
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.1em;
  }
  
  button:hover {
    background-color: #9a1625;
  }
  
  .minho-auth {
    background-color: white;
    color: black;
    border: 2px solid #b21b2d;
    font-weight: bold;
    padding: 0.8em;
    width: 108%; /* Garante que o botão "Autenticação UMinho" também tenha a mesma largura */
    border-radius: 5px;
    cursor: pointer;
    font-size: 1.1em;
    margin-top: 1em;
  }
  
  .minho-auth:hover {
    background-color: #f4f4f4;
    color: #9a1625;
  }
  
  a {
    color: #b21b2d;
    text-decoration: none;
    font-weight: bold;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  .login-container {
    background-color: white;
    padding: 2.5em;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    width: 350px;
  }
  
  h2 {
    font-size: 2em; /* Aumentar o tamanho da fonte do título */
    margin-bottom: 0em;
    font-weight: bold;
    font-family: 'Inter', sans-serif; /* Fonte Inter para o título "Entre na sua conta" */
  }
  
  .footer {
    font-size: 1.2em; /* Ajuste o tamanho do texto do rodapé para equilibrar com o título */
    font-family: 'Inter', sans-serif; /* Fonte Inter para o rodapé */
  }
  
  /* Linha "Ou entrar com" */
  .or-text {
    text-align: center;
    color: #ccc; /* Cor cinza claro */
    margin: 1.5em 0;
    font-weight: normal;
  }
  
  .or-text::before, .or-text::after {
    content: " ";
    display: inline-block;
    width: 45%;
    height: 1px;
    background: #ccc;
    vertical-align: middle;
    margin: 0 10px;
  }
  </style>
  