import { configureStore } from "@reduxjs/toolkit";
// 1. Importujemy niezbędne elementy z redux-persist
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage"; // To domyślnie jest localStorage

import userReducer from "./userState";
import reservationReducer from "./reservationdDraft";
import pagesReducer from "./pageData"; 

const userPersistConfig = {
  key: 'user', 
  storage,     
};

const persistedUserReducer = persistReducer(userPersistConfig, userReducer);

export const store = configureStore({
  reducer: {
    user: persistedUserReducer, 
    reservation: reservationReducer,
    page: pagesReducer,
  },

  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;