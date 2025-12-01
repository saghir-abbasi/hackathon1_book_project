import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';
import customElementStyles from '../../css/custom-elements.module.css'; // Import custom element styles

type ModuleItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
  link: string;
};

const ModuleList: ModuleItem[] = [
  {
    title: 'Module 1: Robotic Nervous System',
    // Placeholder SVG, replace with actual icons later
    Svg: require('@site/static/img/logo.svg').default,
    description: (
      <>
        Dive into the fundamentals of robotic control with ROS 2 and master URDF for robot modeling.
      </>
    ),
    link: '/book/modules/module-1-robotic-nervous-system/chapter-1-ros2-basics',
  },
  {
    title: 'Module 2: Digital Twin',
    Svg: require('@site/static/img/logo.svg').default,
    description: (
      <>
        Explore advanced simulation techniques with Gazebo and Unity for realistic robot environments.
      </>
    ),
    link: '/book/modules/module-2-digital-twin/chapter-1-gazebo-physics',
  },
  {
    title: 'Module 3: AI Robot Brain',
    Svg: require('@site/static/img/logo.svg').default,
    description: (
      <>
        Unleash the power of AI with Isaac Sim for high-fidelity simulations and VSLAM for navigation.
      </>
    ),
    link: '/book/modules/module-3-ai-robot-brain/chapter-1-isaac-sim-basics',
  },
  {
    title: 'Module 4: Vision-Language-Action',
    Svg: require('@site/static/img/logo.svg').default,
    description: (
      <>
        Learn to integrate advanced AI for cognitive planning and speech recognition with Whisper.
      </>
    ),
    link: '/book/modules/module-4-vision-language-action/chapter-1-cognitive-planning',
  },
];

function Module({title, Svg, description, link}: ModuleItem) {
  return (
    <div className={clsx('col col--3', styles.moduleCard)}>
      <div className="text--center">
        <Svg className={styles.moduleSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
        <Link className={clsx('button button--secondary', customElementStyles.mechaPanelButton)} to={link}>
          Explore Module
        </Link>
      </div>
    </div>
  );
}

export default function HomepageModules(): JSX.Element {
  return (
    <section className={styles.modules}>
      <div className="container">
        <Heading as="h2" className="text--center">Book Modules</Heading>
        <div className="row">
          {ModuleList.map((props, idx) => (
            <Module key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

