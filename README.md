¡Perfecto! Vamos a hacerlo **paso a paso, desde cero hasta tener tu propio chatbot de WhatsApp personalizado**, con la capacidad de agregarle **lo que tú quieras** (respuestas, menús, pedidos, soporte, etc.). Usaremos la **WhatsApp Cloud API oficial de Meta**, que es la única forma segura, legal y estable hoy en día.

---

## 🎯 OBJETIVO FINAL:
> Tener un **chatbot de WhatsApp que responda automáticamente** a tus clientes, y que tú puedas **personalizar completamente** (por ejemplo: responder preguntas frecuentes, tomar pedidos, enviar catálogos, etc.).

---

# ✅ PASO A PASO: Cómo Hacer tu Chatbot de WhatsApp (Personalizable)

---

## 🔧 **PASO 1: Preparar tu Entorno (Lo Necesitas Antes de Empezar)**

### ✅ Requisitos previos:
| Elemento | ¿Por qué? |
|--------|-----------|
| 📱 Un número de WhatsApp **empresarial** | No puedes usar tu número personal. Usa uno verificado con **Meta Business Suite** (puedes usar un número virtual como el de Twilio o Vonage). |
| 💻 Una cuenta de **Meta for Developers** | [https://developers.facebook.com/](https://developers.facebook.com/) |
| 🌐 Una URL pública accesible por Internet | Para recibir mensajes de WhatsApp (usaremos Render.com gratis) |
| 🔐 Un token de acceso | Para autenticar tu app con la API de WhatsApp |

> 💡 *Si no tienes un número empresarial, te explico cómo conseguir uno al final.*

---

## 🚀 **PASO 2: Crear tu App en Meta Developer**

1. Ve a: [https://developers.facebook.com/apps/](https://developers.facebook.com/apps/)
2. Haz clic en **“Create App”** → Elige **“Business”** → Nombre: “MiChatbotWhatsApp”
3. En el panel izquierdo, haz clic en **“WhatsApp”** → **“Set up”**
4. Te pedirá conectar una **cuenta de Meta Business Suite**. Si no tienes una:
   - Ve a [https://business.facebook.com/](https://business.facebook.com/)
   - Haz clic en “Crear cuenta empresarial”
   - Conecta tu página de Facebook (si ya tienes una)
5. Ahora vuelve a **Meta Developers → WhatsApp → Set up** → Sigue los pasos para:
   - **Asociar tu número de WhatsApp empresarial** (el que compraste o tienes)
   - **Generar un Token de Acceso** (lo necesitarás más adelante)
6. Copia este valor:  
   👉 **`WHATSAPP_ACCESS_TOKEN`** — Es un string muy largo que empieza con `EAAG...`

7. También copia:  
   👉 **`WHATSAPP_PHONE_NUMBER_ID`** — Lo encuentras en:  
   *WhatsApp → Phone Numbers → Tu número → Copy ID*

---

## 💻 **PASO 3: Crear tu Bot de Prueba (Echo Bot) en Render.com**

Vamos a usar el **“Echo Bot”** de la documentación oficial, pero lo vamos a mejorar para que **responda**.

### ✅ Paso 3.1: Crea un repositorio en GitHub

1. Ve a [https://github.com/](https://github.com/)
2. Haz clic en **“New repository”**
3. Nombre: `mi-chatbot-whatsapp`
4. Público o privado → da igual
5. Haz clic en **“Create repository”**

### ✅ Paso 3.2: Crea el archivo `app.js`

Dentro del repo, haz clic en **“Add file” → “Create new file”**

Nombre del archivo: `app.js`

Pega este código **mejorado** (no el original, porque el original solo recibe, ¡aquí respondemos!):

```js
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
```

> ✅ Este código:
> - Recibe cualquier mensaje
> - Responde con un texto personalizado
> - Está listo para que le agregues lógica después

### ✅ Paso 3.3: Guarda y sube el archivo a GitHub

- Escribe un commit: `Initial commit`
- Haz clic en “Commit new file”

---

## 🌐 **PASO 4: Desplegar tu bot en Render.com (Gratis)**

1. Ve a: [https://render.com/](https://render.com/)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en **“New +” → “Web Service”**
4. Conecta tu repositorio: `mi-chatbot-whatsapp`
5. Configura:
   - **Name**: `mi-chatbot-whatsapp` (o el nombre que quieras)
   - **Region**: North America (o Europa)
   - **Build Command**: `npm install`
   - **Start Command**: `node app.js`
6. En **Environment Variables**, agrega:

| Key | Value |
|-----|-------|
| `VERIFY_TOKEN` | `vibecode` *(elige tu propia palabra, ej: "mipass123")* |
| `WHATSAPP_ACCESS_TOKEN` | `EAAGqZ...` *(el token largo que copiaste de Meta)* |
| `WHATSAPP_PHONE_NUMBER_ID` | `123456789012345` *(el ID de tu número de WhatsApp)* |

> ⚠️ ¡Importante! Estas variables deben llamarse exactamente como en el código (`WHATSAPP_ACCESS_TOKEN`, etc.)

7. Haz clic en **“Create Web Service”**

⏳ Espera 2-5 minutos hasta que veas:  
> ✅ **"Your service is live"**

Copia la URL que aparece arriba:  
👉 `https://mi-chatbot-whatsapp.onrender.com`

---

## 🔗 **PASO 5: Conectar tu Webhook en Meta**

1. Vuelve a [Meta Developers → Tu App → WhatsApp → Configuration](https://developers.facebook.com/apps/)
2. En **Callback URL**, pega:  
   `https://mi-chatbot-whatsapp.onrender.com`
3. En **Verify Token**, pega: `vibecode` (la misma que pusiste en Render)
4. Haz clic en **“Verify and Save”**

✅ Si ves **“Webhook verified”** → ¡Funcionó!

5. **Suscríbete al webhook `messages`**  
   - Marca la casilla de **`messages`** (es clave)
   - Haz clic en **“Save Changes”**

---

## 📲 **PASO 6: Probar tu Chatbot**

1. Abre WhatsApp en tu celular
2. Envía un mensaje a tu **número empresarial de WhatsApp** (el que configuraste en Meta)
3. En unos segundos, deberías recibir una respuesta automática como:

```
🤖 Gracias por escribir: "Hola"

¿Qué necesitas?
1. Pedidos
2. Soporte
3. Horarios

Responde con el número.
```

4. Ve a Render → Logs → Verás el mensaje recibido y el enviado.

🎉 ¡Felicidades! Tu chatbot está funcionando.

---

## 🛠️ **PASO 7: ¡Personaliza tu Chatbot! (Lo que tú quieras)**

Ahora viene lo mejor: **tú decides qué hace tu bot**.

### 💡 Ejemplo 1: Menú interactivo con botones

Modifica esta parte en `app.js`:

```js
await sendWhatsAppMessage(phoneNumber, `
👋 ¡Hola! ¿En qué puedo ayudarte?

Elige una opción:
1. 🛒 Realizar pedido
2. ℹ️ Información de productos
3. 🕒 Horarios de atención
4. 📞 Contactar a un humano
`);
```

### 💡 Ejemplo 2: Responder según palabras clave

Agrega esto dentro de `app.post('/', async (req, res) => { ... })`:

```js
if (text.toLowerCase().includes('hola') || text.toLowerCase().includes('hi')) {
  await sendWhatsAppMessage(phoneNumber, '¡Hola! 😊 Bienvenido a mi tienda. ¿Necesitas ayuda con algo?');
} else if (text.includes('pedido')) {
  await sendWhatsAppMessage(phoneNumber, 'Para hacer un pedido, envía: *pedido [nombre producto]*\nEj: pedido camiseta roja');
} else if (text.includes('horario')) {
  await sendWhatsAppMessage(phoneNumber, 'Estamos abiertos de Lunes a Viernes: 9:00 - 18:00\nSábados: 10:00 - 16:00');
} else {
  await sendWhatsAppMessage(phoneNumber, 'No entendí tu mensaje. ¿Puedes reescribirlo?');
}
```

### 💡 Ejemplo 3: Enviar imágenes o catálogo

```js
await sendWhatsAppMessage(phoneNumber, 'Aquí tienes nuestro catálogo:');
// Luego usa tipo "image"
await sendWhatsAppImage(phoneNumber, "https://tudominio.com/catalogo.jpg");
```

Y agrega esta función:

```js
async function sendWhatsAppImage(to, imageUrl) {
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
      type: 'image',
      image: {
        link: imageUrl
      }
    })
  });
  const result = await response.json();
  if (!response.ok) console.error("Error enviando imagen:", result);
}
```

### 💡 Ejemplo 4: Usar plantillas aprobadas (para mensajes automáticos)

Si quieres enviar un mensaje como:  
> “Tu pedido #123 ha sido confirmado”

Debes primero **aprobar la plantilla** en Meta:

1. Ve a: **WhatsApp → Message Templates**
2. Haz clic en **“Create Template”**
3. Nombre: `order_confirmed`
4. Idioma: `es_ES`
5. Contenido:
   ```
   Tu pedido {{1}} ha sido confirmado. Llegará en {{2}} días.
   ```
6. Envía para aprobación (tarda 1-3 días)

Luego, en tu código:

```js
await sendWhatsAppTemplate(phoneNumber, "order_confirmed", ["123", "2"]);
```

Y agrega:

```js
async function sendWhatsAppTemplate(to, templateName, parameters) {
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
      type: 'template',
      template: {
        name: templateName,
        language: { code: 'es_ES' },
        components: [
          {
            type: 'body',
            parameters: parameters.map(p => ({ type: 'text', text: p }))
          }
        ]
      }
    })
  });
  const result = await response.json();
  if (!response.ok) console.error("Error plantilla:", result);
}
```

---

## 📦 BONUS: ¿Cómo obtener un número de WhatsApp empresarial?

Si aún no tienes uno:

### Opción 1: Usa un número virtual (Recomendado)
- Regístrate en [Twilio](https://www.twilio.com/) → Busca “WhatsApp Sandbox”
- Te dan un número temporal de prueba (solo para pruebas)
- Puedes probar sin pagar

### Opción 2: Compra un número real (Producción)
- Usa [Twilio](https://www.twilio.com/) o [Vonage](https://www.vonage.com/)
- Compra un número de teléfono (ej: +52 55 1234 5678)
- Vincúlalo a tu cuenta de Meta Business Suite

> ✅ Solo números **verificados por Meta** pueden enviar mensajes fuera del sandbox.

---

## 🚀 PROXIMOS PASOS (Escalabilidad)

| Qué quieres hacer | Cómo lograrlo |
|-------------------|---------------|
| Guardar conversaciones | Usa SQLite o PostgreSQL para guardar `(numero, mensaje, respuesta)` |
| Manejar múltiples usuarios | Usa el campo `from` como identificador único |
| Integrar con tu web | Crea un formulario en tu sitio y envía a WhatsApp |
| Automatizar ventas | Usa Google Sheets + Zapier o Airtable para registrar pedidos |
| Notificaciones automáticas | Programa tareas con cron jobs (Render tiene planos de pago para esto) |
