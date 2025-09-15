const express = require('express');
const app = express();
const fetch = require('node-fetch'); // Para llamar a la API de WhatsApp

app.use(express.json());

const PORT = process.env.PORT || 3000;
const VERIFY_TOKEN = process.env.VERIFY_TOKEN; // Tu palabra secreta
const WHATSAPP_TOKEN = process.env.WHATSAPP_ACCESS_TOKEN; // Token de Meta
const PHONE_NUMBER_ID = process.env.WHATSAPP_PHONE_NUMBER_ID; // ID del número

// Ruta para verificar webhook (GET)
app.get('/', (req, res) => {
  const { 'hub.mode': mode, 'hub.verify_token': token, 'hub.challenge': challenge } = req.query;
  if (mode === 'subscribe' && token === VERIFY_TOKEN) {
    console.log('✅ WEBHOOK VERIFICADO');
    res.status(200).send(challenge);
  } else {
    console.log('❌ Verificación fallida');
    res.status(403).end();
  }
});

// Ruta para recibir mensajes (POST)
app.post('/', async (req, res) => {
  const body = req.body;

  // Verifica si hay mensajes entrantes
  if (body.entry && body.entry[0].changes && body.entry[0].changes[0].value.messages) {
    const message = body.entry[0].changes[0].value.messages[0];
    const phoneNumber = message.from; // Número del usuario
    const text = message.text?.body;   // Texto que envió el usuario

    if (text) {
      console.log(`💬 Recibido de ${phoneNumber}: ${text}`);

      // 🚀 RESPONDE AUTOMÁTICAMENTE
      await sendWhatsAppMessage(phoneNumber, `🤖 Gracias por escribir: "${text}"\n\n¿Qué necesitas?\n1. Pedidos\n2. Soporte\n3. Horarios\n\nResponde con el número.`);
    }
  }

  res.status(200).end();
});

// Función para enviar mensaje por WhatsApp
async function sendWhatsAppMessage(to, messageText) {
  const url = `https://graph.facebook.com/v20.0/${PHONE_NUMBER_ID}/messages`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${WHATSAPP_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messaging_product: 'whatsapp',
      to: to,
      type: 'text',
      text: { body: messageText }
    })
  });

  const result = await response.json();
  if (response.ok) {
    console.log(`📤 Mensaje enviado a ${to}: ${messageText}`);
  } else {
    console.error('❌ Error enviando mensaje:', result);
  }
}

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
});