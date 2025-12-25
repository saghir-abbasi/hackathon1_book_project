import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "Physical AI & Humanoid Robotics",
  tagline: "Mastering Intelligent Robot Design and Operation",
  favicon: "img/favicon.svg",

  // Head tags for external resources
  headTags: [
    {
      tagName: "link",
      attributes: {
        rel: "preconnect",
        href: "https://fonts.googleapis.com",
      },
    },
    {
      tagName: "link",
      attributes: {
        rel: "preconnect",
        href: "https://fonts.gstatic.com",
        crossorigin: "anonymous",
      },
    },
    {
      tagName: "link",
      attributes: {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap",
      },
    },
  ],
  // GitHub Pages Configuration
  // https://saghir-abbasi.github.io/book_project/
  // url: "https://saghir-abbasi.github.io", // your GitHub Pages root URL
  url: "https://saghir-abbasi.github.io",
  baseUrl: "/book_project/", // repo name with leading & trailing slash
  organizationName: "saghir-abbasi", // GitHub username or org
  projectName: "book_project", // repo nam
  // deploymentBranch: "gh-pages",
  trailingSlash: false,

  onBrokenLinks: "throw",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          path: "./docs/book-content-internal",
          routeBasePath: "/book",
          editUrl: undefined,
          exclude: ["shared/templates/**/*.mdx", "README.md"],
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ["rss", "atom"],
            xslt: true,
          },
          editUrl:
            "https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/",
          onInlineTags: "warn",
          onInlineAuthors: "warn",
          onUntruncatedBlogPosts: "warn",
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: "img/docusaurus-social-card.jpg",
    colorMode: {
      respectPrefersColorScheme: true,
      defaultMode: "dark",
    },
    navbar: {
      title: "Physical AI & Robotics",
      logo: {
        alt: "Physical AI & Robotics Logo",
        src: "img/logo.svg",
      },
      items: [
        // Navigation items removed - using custom navbar with auth
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Book",
          items: [
            {
              label: "Start Reading",
              to: "/book/modules/module-1-robotic-nervous-system/chapter-1-ros2-basics",
            },
          ],
        },
        {
          title: "Community",
          items: [
            {
              label: "Stack Overflow",
              href: "https://stackoverflow.com/questions/tagged/robotics",
            },
            {
              label: "Discord",
              href: "https://discordapp.com/invite/docusaurus",
            },
          ],
        },
        {
          title: "Resources",
          items: [
            {
              label: "ROS2 Documentation",
              href: "https://docs.ros.org/en/humble/",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Saghir Abbasi. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
