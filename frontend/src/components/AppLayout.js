import React from 'react';
import AppHeader from './AppHeader';
import AppFooter from './AppFooter';

// children 속성으로 Layout안 출력
function AppLayout({children}) {
    return (
        <>
            <AppHeader />
            {children}
            <AppFooter />
        </>
    )
}

export default AppLayout;