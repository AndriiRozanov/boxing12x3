export default function middleware(request) {
  const url = new URL(request.url);

  if (url.pathname === '/' && url.searchParams.get('lang') === 'en' && !url.searchParams.has('widget')) {
    return Response.redirect(new URL('/en', url.origin), 308);
  }

  if (url.pathname === '/height-compare' && url.searchParams.get('lang') === 'en') {
    return Response.redirect(new URL('/en/height-compare', url.origin), 308);
  }

  if (url.pathname === '/ua/charlo-mazoudier' || url.pathname === '/en/charlo-mazoudier') {
    return Response.redirect(new URL(url.pathname.replace('charlo-mazoudier', 'resendiz-mazoudier'), url.origin), 308);
  }

  return fetch(request);
}

export const config = {
  matcher: ['/', '/height-compare', '/ua/charlo-mazoudier', '/en/charlo-mazoudier'],
};
