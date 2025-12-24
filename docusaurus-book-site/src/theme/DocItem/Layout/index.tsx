import React from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type { WrapperProps } from '@docusaurus/types';
import ChapterToolbar from '@site/src/components/ChapterToolbar';

type Props = WrapperProps<typeof LayoutType>;

/**
 * Swizzled DocItem/Layout wrapper.
 * Adds ChapterToolbar with Personalize and Translate buttons above doc content.
 */
export default function LayoutWrapper(props: Props): JSX.Element {
  return (
    <>
      <ChapterToolbar />
      <Layout {...props} />
    </>
  );
}
