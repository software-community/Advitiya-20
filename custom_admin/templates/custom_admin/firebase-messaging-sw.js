// [START initialize_firebase_in_sw]
// Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/7.7.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.7.0/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.
firebase.initializeApp({
  apiKey: "AIzaSyDbNJ--j-m1WNrMxSHys81rjseH4FMuHys",
  authDomain: "advitiya2020-719da.firebaseapp.com",
  databaseURL: "https://advitiya2020-719da.firebaseio.com",
  projectId: "advitiya2020-719da",
  storageBucket: "advitiya2020-719da.appspot.com",
  messagingSenderId: "598295117177",
  appId: "1:598295117177:web:946a6512b805df9b0203a8",
  measurementId: "G-WRN5HSTQL9"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
// [END initialize_firebase_in_sw]

// If you would like to customize notifications that are received in the
// background (Web app is closed or not in browser focus) then you should
// implement this optional method.
// [START background_handler]
messaging.setBackgroundMessageHandler(function (payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
});
// [END background_handler]
