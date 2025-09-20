import { create } from "zustand";

export type ToastKind = "success" | "error" | "info";

type ToastState = {
  open: boolean;
  message: string;
  kind: ToastKind;
  show: (message: string, kind?: ToastKind) => void;
  hide: () => void;
};

export const useToastStore = create<ToastState>((set) => ({
  open: false,
  message: "",
  kind: "info",
  show: (message, kind = "info") => set({ open: true, message, kind }),
  hide: () => set({ open: false }),
}));
