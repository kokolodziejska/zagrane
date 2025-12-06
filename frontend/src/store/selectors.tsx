import type { RootState } from './store';

export const selectPickedDate = (state: RootState) => state.user.pickedDate;
export const selectIsLogin = (state: RootState) => state.user.isLogin;
export const selectUserId = (state: RootState) => state.user.userId;
export const selectUserName = (state: RootState) => state.user.userName;
export const selectUserSurname = (state: RootState) => state.user.userSurname;
export const selectStartHour = (state: RootState) => state.user.pickedStartHour;
export const selectObjectId = (state: RootState) => state.user.pickedObjectId;

export const selectReservationDraft = (state: RootState) => state.reservation;

export const selectPages = (state: RootState) => state.page.pages;
export const selectPagesLoading = (state: RootState) => state.page.loading;
export const selectPagesError = (state: RootState) => state.page.error;
