import DefaultTheme from "vitepress/theme";
import type { Theme } from "vitepress";
import HomeCourseMatrix from "./components/HomeCourseMatrix.vue";
import HomeEvidenceFlow from "./components/HomeEvidenceFlow.vue";
import HomeGithubPanel from "./components/HomeGithubPanel.vue";
import HomeLaunchPads from "./components/HomeLaunchPads.vue";
import HomePathExplorer from "./components/HomePathExplorer.vue";
import HomeSystemMap from "./components/HomeSystemMap.vue";
import "./custom.css";

const theme: Theme = {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component("HomeCourseMatrix", HomeCourseMatrix);
    app.component("HomeEvidenceFlow", HomeEvidenceFlow);
    app.component("HomeGithubPanel", HomeGithubPanel);
    app.component("HomeLaunchPads", HomeLaunchPads);
    app.component("HomePathExplorer", HomePathExplorer);
    app.component("HomeSystemMap", HomeSystemMap);
  },
};

export default theme;
