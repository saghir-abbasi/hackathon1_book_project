import type {ReactNode} from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import HomepageModules from '@site/src/components/HomepageModules'; // Import the new component
import Heading from '@theme/Heading';
import { ProtectedLink } from '@site/src/components/Auth';

import styles from './index.module.css';
import customElementStyles from '../css/custom-elements.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={customElementStyles.aiGridBackground}></div>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <ProtectedLink
            className={clsx('button button--secondary button--lg', customElementStyles.mechaPanelButton)}
            to="/book_project/book/modules/module-1-robotic-nervous-system/chapter-1-ros2-basics">
            Start Reading 📖
          </ProtectedLink>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <HomepageModules /> {/* Render the new component */}
      </main>
    </Layout>
  );
}
