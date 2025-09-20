import { create } from "zustand";

type UploadState = {
  taskId: string | null;
  setTaskId: (id: string | null) => void;
};

export const useUploadStore = create<UploadState>((set) => ({
  taskId: null,
  setTaskId: (id) => set({ taskId: id }),
}));
