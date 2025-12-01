import React from 'react';
import type RootType from '@theme/Root';
import Chatbot from '../components/chatbot'; // Adjust path if needed

// Default implementation, that you might want to customize
function Root(props: Parameters<typeof RootType>[0]) {
  return (
    <>
      <Chatbot />
      {props.children}
    </>
  );
}

export default Root;
