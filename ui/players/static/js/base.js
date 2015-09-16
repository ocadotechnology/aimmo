'use strict';

var messages = {
  common: {
    program: "Program",
    watch: "Watch",
    stats: "Statistics",
    startGame: "Start Game",
    login: "Login",
    logout: "Logout",
    register: "Register",
    noAccount: "Don't have an account?",
    usernameOrEmail: "Username or Email",
    username: "Username",
    password: "Password",
    passwordConfirmation: "Password Confirmation",
  }

}

$('.aimmo-messages-program').text(messages.common.program);
$('.aimmo-messages-watch').text(messages.common.watch);
$('.aimmo-messages-stats').text(messages.common.stats);
$('.aimmo-messages-start-game').text(messages.common.startGame);
$('.aimmo-messages-login').text(messages.common.login);
$('.aimmo-messages-logout').text(messages.common.logout);
$('.aimmo-messages-register').text(messages.common.register);
$('.aimmo-messages-no-account').text(messages.common.noAccount);
$('.aimmo-messages-username-or-email').attr('placeholder', messages.common.usernameOrEmail);
$('.aimmo-messages-bg-password').attr('placeholder', messages.common.password);
$('.aimmo-messages-password').text(messages.common.password);
$('.aimmo-messages-bg-username').attr('placeholder', messages.common.username);
$('.aimmo-messages-username').text(messages.common.username);
$('.aimmo-messages-bg-password-confirmation').attr('placeholder', messages.common.passwordConfirmation);
$('.aimmo-messages-password-confirmation').text(messages.common.passwordConfirmation);



