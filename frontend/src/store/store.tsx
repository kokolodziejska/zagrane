import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./userState";
import reservationReducer from "./reservationdDraft";
import pagesReducer from "./pageData"; 

export const store = configureStore({
  reducer: {
    user: userReducer,
    reservation: reservationReducer,
    page: pagesReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
