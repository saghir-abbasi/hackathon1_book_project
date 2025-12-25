import React from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type { WrapperProps } from '@docusaurus/types';

type Props = WrapperProps<typeof LayoutType>;

/**
 * Swizzled DocItem/Layout wrapper.
 * ChapterToolbar has been moved to the navbar for better UX.
 */
export default function LayoutWrapper(props: Props): JSX.Element {
  return <Layout {...props} />;
}
