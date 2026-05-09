<template>
  <div class="window no-resize" name="Open ZIP">
    <div class="box">
      <p v-if="autoLoading">{{ autoLoadStatus }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useXashStore } from "/@/stores/store";
import { storeToRefs } from "pinia";
import { XashLoader } from "/@/services";

const store = useXashStore();
const autoLoading = ref(true);
const autoLoadStatus = ref("waiting for canvas...");

const {
  selectedGame,
  xashCanvas,
  selectedZip,
  launchOptions,
  selectedLocalFolder,
  fullScreen,
  enableConsole,
  enableCheats,
  loadingProgress,
  customGameArg,
} = storeToRefs(store);
const { onStartLoading, onEndLoading, refreshSavesList } = store;

const autoLoad = async () => {
  try {
    autoLoadStatus.value = "downloading valve.zip...";
    const res = await fetch("https://media.githubusercontent.com/media/Noachium/temp.cx/main/fun/HalfLife/public/valve.zip");
    const buffer = await res.arrayBuffer();

    autoLoadStatus.value = "loading into browser...";

    const xash = await XashLoader.startGameZip(buffer, {
      canvas: xashCanvas.value!,
      selectedGame: selectedGame.value,
      selectedZip: selectedZip.value,
      selectedLocalFolder: selectedLocalFolder.value,
      launchOptions: launchOptions.value,
      fullScreen: fullScreen.value,
      enableConsole: enableConsole.value,
      enableCheats: enableCheats.value,
      onStartLoading,
      onEndLoading,
      onProgress: (progress) => {
        loadingProgress.value = typeof progress === "number" ? progress : progress.current;
      },
    });

    await XashLoader.onAfterLoad({
      xash,
      selectedGame: selectedGame.value,
      customGameArg: customGameArg.value,
      enableCheats: enableCheats.value,
    });

    await XashLoader.initConsoleCallbacks(xash, selectedGame.value.consoleCallbacks);
    await refreshSavesList();
    autoLoading.value = false;
  } catch (error) {
    console.error("failed to auto load zip:", error);
    autoLoadStatus.value = "failed to load, check console";
  }
};

onMounted(async () => {
  if (!xashCanvas.value) {
    const stop = watch(xashCanvas, async (canvas) => {
      if (canvas) {
        stop();
        await autoLoad();
      }
    });
  } else {
    await autoLoad();
  }
});
</script>

<style scoped lang="scss">
.start-button {
  text-align: center;
  width: 100%;
}
</style>