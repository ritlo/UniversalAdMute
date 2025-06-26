document.addEventListener("DOMContentLoaded", () => {
  const startButton = document.getElementById("startButton");
  const stopButton = document.getElementById("stopButton");
  const saveSettingsButton = document.getElementById("saveSettingsButton");

  const mutingActiveStatus = document.getElementById("mutingActiveStatus");
  const audioUnmutedStatus = document.getElementById("audioUnmutedStatus");
  const currentVolumeStatus = document.getElementById("currentVolumeStatus");

  const adPromptInput = document.getElementById("adPrompt");
  const contentPromptInput = document.getElementById("contentPrompt");
  const adPromptList = document.getElementById("adPromptList");
  const contentPromptList = document.getElementById("contentPromptList");

  let API_BASE_URL;

  const MAX_RECENT_PROMPTS = 10;

  function getRecentPrompts(key) {
    const prompts = localStorage.getItem(key);
    return prompts ? JSON.parse(prompts) : [];
  }

  function addRecentPrompt(key, prompt) {
    if (!prompt) return;
    let prompts = getRecentPrompts(key);
    prompts = prompts.filter((p) => p !== prompt); 
    prompts.unshift(prompt); 
    if (prompts.length > MAX_RECENT_PROMPTS) {
      prompts = prompts.slice(0, MAX_RECENT_PROMPTS); 
    }
    localStorage.setItem(key, JSON.stringify(prompts));
  }

  function populateDatalist(datalistElement, prompts) {
    datalistElement.innerHTML = "";
    prompts.forEach((prompt) => {
      const option = document.createElement("option");
      option.value = prompt;
      datalistElement.appendChild(option);
    });
  }

  function loadSavedState() {
    const savedAdPrompt = localStorage.getItem("currentAdPrompt");
    const savedContentPrompt = localStorage.getItem("currentContentPrompt");
    if (savedAdPrompt) {
      adPromptInput.value = savedAdPrompt;
    }
    if (savedContentPrompt) {
      contentPromptInput.value = savedContentPrompt;
    }
    populateDatalist(adPromptList, getRecentPrompts("recentAdPrompts"));
    populateDatalist(
      contentPromptList,
      getRecentPrompts("recentContentPrompts")
    );
  }

  adPromptInput.addEventListener("input", () => {
    localStorage.setItem("currentAdPrompt", adPromptInput.value);
  });

  contentPromptInput.addEventListener("input", () => {
    localStorage.setItem("currentContentPrompt", contentPromptInput.value);
  });

  async function loadApiConfig() {
    try {
      const response = await fetch("http://127.0.0.1:32542/config");
      const data = await response.json();
      API_BASE_URL = `http://${data.api_host}:${data.api_port}`;
      console.log(`API Base URL set to: ${API_BASE_URL}`);
    } catch (error) {
      console.error("Error loading API config:", error);
      API_BASE_URL = "http://127.0.0.1:32542";
      console.warn(`Falling back to default API Base URL: ${API_BASE_URL}`);
    }
  }

  async function fetchStatus() {
    try {
      const response = await fetch(`${API_BASE_URL}/status`);
      const data = await response.json();
      mutingActiveStatus.textContent = data.muting_active ? "Yes" : "No";
      audioUnmutedStatus.textContent = data.is_unmuted ? "Yes" : "No";
      currentVolumeStatus.textContent =
        data.current_volume !== undefined
          ? `${(data.current_volume * 100).toFixed(0)}%`
          : "N/A";

      if (
        document.activeElement !== adPromptInput &&
        adPromptInput.value !== (data.text_prompts[0] || "")
      ) {
        adPromptInput.value = data.text_prompts[0] || "";
        localStorage.setItem("currentAdPrompt", adPromptInput.value);
      }
      if (
        document.activeElement !== contentPromptInput &&
        contentPromptInput.value !== (data.text_prompts[1] || "")
      ) {
        contentPromptInput.value = data.text_prompts[1] || "";
        localStorage.setItem("currentContentPrompt", contentPromptInput.value);
      }

      startButton.disabled = data.muting_active;
      stopButton.disabled = !data.muting_active;
    } catch (error) {
      console.error("Error fetching status:", error);
      mutingActiveStatus.textContent = "API Error";
      audioUnmutedStatus.textContent = "API Error";
      currentVolumeStatus.textContent = "API Error";
      startButton.disabled = true;
      stopButton.disabled = true;
    }
  }

  startButton.addEventListener("click", async () => {
    startButton.disabled = true;
    stopButton.disabled = true;
    try {
      const response = await fetch(`${API_BASE_URL}/start`);
      const data = await response.json();
      if (response.ok) {
        console.log(data.status);
        fetchStatus();
      } else {
        console.error(
          "Error starting muting:",
          data.detail || response.statusText
        );
        alert(`Error: ${data.detail || response.statusText}`);
        fetchStatus();
      }
    } catch (error) {
      console.error("Network error starting muting:", error);
      alert("Network error: Could not connect to the backend server.");
      fetchStatus();
    }
  });

  stopButton.addEventListener("click", async () => {
    stopButton.disabled = true;
    startButton.disabled = true;
    try {
      const response = await fetch(`${API_BASE_URL}/stop`);
      const data = await response.json();
      if (response.ok) {
        console.log(data.status);
        fetchStatus();
      } else {
        console.error(
          "Error stopping muting:",
          data.detail || response.statusText
        );
        alert(`Error: ${data.detail || response.statusText}`);
        fetchStatus();
      }
    } catch (error) {
      console.error("Network error stopping muting:", error);
      alert("Network error: Could not connect to the backend server.");
      fetchStatus();
    }
  });

  saveSettingsButton.addEventListener("click", async () => {
    saveSettingsButton.disabled = true;
    try {
      const newConfig = {
        text_prompts: [adPromptInput.value, contentPromptInput.value],
      };
      const response = await fetch(`${API_BASE_URL}/settings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newConfig),
      });
      const data = await response.json();
      if (response.ok) {
        console.log(data.status, data.new_config);
        alert("Settings saved successfully!");
        addRecentPrompt("recentAdPrompts", adPromptInput.value);
        addRecentPrompt("recentContentPrompts", contentPromptInput.value);
        populateDatalist(adPromptList, getRecentPrompts("recentAdPrompts"));
        populateDatalist(
          contentPromptList,
          getRecentPrompts("recentContentPrompts")
        );
        fetchStatus();
      } else {
        console.error(
          "Error saving settings:",
          data.detail || response.statusText
        );
        alert(`Failed to save settings: ${data.detail || response.statusText}`);
      }
    } catch (error) {
      console.error("Network error saving settings:", error);
      alert("Network error: Could not connect to the backend server.");
    } finally {
      saveSettingsButton.disabled = false;
    }
  });

  (async () => {
    loadSavedState();
    await loadApiConfig();
    fetchStatus();
    setInterval(fetchStatus, 5000);
  })();
});
