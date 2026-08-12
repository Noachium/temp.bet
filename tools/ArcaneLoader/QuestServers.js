Il2Cpp.perform(() => {
  function findClass(className) {
    for (const assembly of Il2Cpp.domain.assemblies) {
      try {
        const klass = assembly.image.tryClass(className);
        if (klass) return klass;
      } catch (_) {}
    }
    return null;
  }

  const appUtils = findClass("AnimalCompany.AppUtils");
  if (!appUtils) {
    console.error("[Quest Servers] Could not find AnimalCompany.AppUtils class");
    return;
  }

  const versionMethod = appUtils.methods.find(
    m =>
      /CalculatePhotonAppVersion/i.test(m.name) &&
      (m.returnType?.name ?? "") === "System.String"
  );
  if (!versionMethod) {
    console.error("[Quest Servers] Could not find CalculatePhotonAppVersion");
    return;
  }

  Interceptor.attach(versionMethod.virtualAddress, {
    onEnter(args) {
      try {
        args[2] = ptr(1);
      } catch (_) {}
    },
    onLeave(retval) {
      try {
        console.log("[Quest Servers Debug] Photon App Version: " + new Il2Cpp.String(retval).content);
      } catch (_) {}
    },
  });

  console.log("[Quest Servers] Auto updating quest servers loaded!");
});