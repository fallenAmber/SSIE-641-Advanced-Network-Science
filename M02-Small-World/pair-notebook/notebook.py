# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "igraph",
#     "networkx",
#     "matplotlib",
#     "seaborn",
#     "altair",
#     "anywidget",
#     "traitlets",
#     "numpy",
#     "pandas",
#     "pillow",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", css_file="lecture-hall.css")


@app.cell(hide_code=True)
def _(mo):
    # One single string literal on purpose: marimo round-trips mo.md cells
    # through its markdown serializer, and implicit string concatenation
    # corrupts them (the code itself gets wrapped as markdown content).
    mo.md(r"""
    <p style="text-align:right; color:#6A6D75; font-size:12px; margin:0;">🐛 Something broken or odd? Email Prof. Sadamori Kojaku &middot; <a href="mailto:skojaku@binghamton.edu" style="color:#3959A6;">skojaku@binghamton.edu</a></p>
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _():
    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    import seaborn as sns

    # Match figures to the lecture-hall notebook theme (lecture-hall.css).
    # seaborn first (set_theme resets rc), then our palette on top.
    sns.set_theme(style="ticks")
    plt.rcParams.update(
        {
            "figure.facecolor": "#FFFDF7",
            "axes.facecolor": "#FFFDF7",
            "savefig.facecolor": "#FFFDF7",
            "text.color": "#35373C",
            "axes.edgecolor": "#1D1E21",
            "axes.labelcolor": "#35373C",
            "axes.titlecolor": "#1D1E21",
            "xtick.color": "#35373C",
            "ytick.color": "#35373C",
            # Axis labels are read, not felt: the same system sans the page
            # prose uses (lecture-hall.css --lh-sans), one entry per platform.
            # A handwriting face here made every number on every chart harder
            # to read than the one thing it is there to say. DejaVu closes the
            # list, which is what stops matplotlib warning on Linux.
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Segoe UI",
                "Helvetica Neue",
                "Helvetica",
                "Arial",
                "Liberation Sans",
                "DejaVu Sans",
            ],
            # path.sketch is what draws by hand, and it is the ONLY thing that
            # does: every line, spine and tick is displaced by (scale, length,
            # randomness). Text is not a path, so the labels stay crisp.
            "path.sketch": (1.1, 110, 2),
            "lines.linewidth": 2.2,
            "axes.linewidth": 1.8,
            "xtick.major.width": 1.4,
            "ytick.major.width": 1.4,
            "axes.spines.top": False,
            "axes.spines.right": False,
            # The accents are the lecture slides' own, verbatim
            # (adv-net-sci/slides/m02/figures/make_figures.py): #3959A6 is the
            # object under discussion, #B14434 what THIS figure is about,
            # #DAB167 the comparison object. A student meeting the same idea in
            # the lecture and in this notebook meets it in the same colour.
            # #3959A6 leads the cycle because a one-series chart draws in the
            # first entry, and that chart's line should be the slides' blue —
            # the darker #22336B is page chrome (links, buttons, focus rings).
            "axes.prop_cycle": plt.cycler(
                color=["#3959A6", "#B14434", "#22336B", "#DAB167", "#6A6D75"]
            ),
        }
    )
    sns.set_palette(["#3959A6", "#B14434", "#22336B", "#DAB167", "#6A6D75"])
    return np, nx, plt


@app.cell(hide_code=True)
def _():
    import altair as alt
    import igraph as ig
    import pandas as pd

    # Altair draws its own type, so without this a chart would letter itself
    # in Vega's default face instead of the page's.
    #
    # The theme has to build its own dict. marimo renames a cell's private
    # names (_face becomes _cell_XXXX_face) and Altair calls the theme back
    # when a chart renders, long after this cell has finished — a closure
    # over a cell local raises NameError at chart time. Everything the
    # function needs is therefore local to it.
    def _lecture_hall_chart_theme():
        # The page's own stack (lecture-hall.css --lh-sans). A chart's labels
        # are read the same way its prose is.
        face = (
            'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", '
            '"Noto Sans", "Liberation Sans", Arial, sans-serif'
        )
        return {
            "config": {
                "font": face,
                "background": "#FFFDF7",
                "view": {"stroke": "transparent"},
                "axis": {
                    "labelFont": face,
                    "titleFont": face,
                    "labelColor": "#35373C",
                    "titleColor": "#1D1E21",
                    "domainColor": "#1D1E21",
                    "domainWidth": 1.8,
                    "tickColor": "#1D1E21",
                    "gridColor": "#D9D2C2",
                },
                "legend": {"labelFont": face, "titleFont": face},
                "title": {"font": face, "fontSize": 15, "color": "#1D1E21", "anchor": "start"},
            }
        }

    try:  # Altair >= 5.5
        alt.theme.register("lecture_hall", enable=True)(_lecture_hall_chart_theme)
    except AttributeError:  # Altair < 5.5
        alt.themes.register("lecture_hall", _lecture_hall_chart_theme)
        alt.themes.enable("lecture_hall")
    return alt, ig, pd


@app.cell(hide_code=True)
def _():
    import anywidget as _anywidget
    import traitlets as _traitlets

    class _NetViz(_anywidget.AnyWidget):
        _esm = r"""
    // ---------------------------------------------------------------------------
    // VENDORED THIRD-PARTY JAVASCRIPT — do not hand-edit; see DESIGN.md principle 8.
    //
    // These used to be two import statements pointing at the esm.sh CDN, which
    // meant every network drawing in the notebook was fetched from a CDN at render
    // time: a student reopening this on a plane, or after esm.sh has moved on, got
    // blank cells. The Python half of "zero setup, forever" was kept by the PEP 723
    // header; this is the JavaScript half.
    //
    // Only what netviz actually calls is here, not all of d3 — d3-selection,
    // d3-drag and d3-force, which is 47 KB instead of 283 KB. IF YOU ADD A d3 CALL
    // TO netviz, CHECK IT IS IN THIS SUBSET: anything else is undefined at runtime,
    // and the figure fails in the browser where Python tests cannot see it.
    // Each library is wrapped in an IIFE because these are minified bundles that
    // would otherwise collide on their short top-level names.
    //
    //   d3-selection 3.x, d3-drag 3.x, d3-force 3.x  — ISC, (c) Mike Bostock
    //   roughjs 4.6.6                                — MIT, (c) Preet Shihn
    //   Fetched from esm.sh (?bundle&target=es2022).
    // ---------------------------------------------------------------------------
    const d3 = Object.assign({}, (()=>{
    /* esm.sh - d3-selection@3.0.0 */
    var E="http://www.w3.org/1999/xhtml",N={svg:"http://www.w3.org/2000/svg",xhtml:E,xlink:"http://www.w3.org/1999/xlink",xml:"http://www.w3.org/XML/1998/namespace",xmlns:"http://www.w3.org/2000/xmlns/"};function x(t){var e=t+="",r=e.indexOf(":");return r>=0&&(e=t.slice(0,r))!=="xmlns"&&(t=t.slice(r+1)),N.hasOwnProperty(e)?{space:N[e],local:t}:t}function Vt(t){return function(){var e=this.ownerDocument,r=this.namespaceURI;return r===E&&e.documentElement.namespaceURI===E?e.createElement(t):e.createElementNS(r,t)}}function Ft(t){return function(){return this.ownerDocument.createElementNS(t.space,t.local)}}function d(t){var e=x(t);return(e.local?Ft:Vt)(e)}function Bt(){}function g(t){return t==null?Bt:function(){return this.querySelector(t)}}function H(t){typeof t!="function"&&(t=g(t));for(var e=this._groups,r=e.length,i=new Array(r),n=0;n<r;++n)for(var o=e[n],f=o.length,l=i[n]=new Array(f),u,s,c=0;c<f;++c)(u=o[c])&&(s=t.call(u,u.__data__,c,o))&&("__data__"in u&&(s.__data__=u.__data__),l[c]=s);return new a(i,this._parents)}function v(t){return t==null?[]:Array.isArray(t)?t:Array.from(t)}function Mt(){return[]}function V(t){return t==null?Mt:function(){return this.querySelectorAll(t)}}function Tt(t){return function(){return v(t.apply(this,arguments))}}function U(t){typeof t=="function"?t=Tt(t):t=V(t);for(var e=this._groups,r=e.length,i=[],n=[],o=0;o<r;++o)for(var f=e[o],l=f.length,u,s=0;s<l;++s)(u=f[s])&&(i.push(t.call(u,u.__data__,s,f)),n.push(u));return new a(i,n)}function F(t){return function(){return this.matches(t)}}function L(t){return function(e){return e.matches(t)}}var Pt=Array.prototype.find;function qt(t){return function(){return Pt.call(this.children,t)}}function Dt(){return this.firstElementChild}function X(t){return this.select(t==null?Dt:qt(typeof t=="function"?t:L(t)))}var It=Array.prototype.filter;function Ot(){return Array.from(this.children)}function kt(t){return function(){return It.call(this.children,t)}}function z(t){return this.selectAll(t==null?Ot:kt(typeof t=="function"?t:L(t)))}function Y(t){typeof t!="function"&&(t=F(t));for(var e=this._groups,r=e.length,i=new Array(r),n=0;n<r;++n)for(var o=e[n],f=o.length,l=i[n]=[],u,s=0;s<f;++s)(u=o[s])&&t.call(u,u.__data__,s,o)&&l.push(u);return new a(i,this._parents)}function b(t){return new Array(t.length)}function K(){return new a(this._enter||this._groups.map(b),this._parents)}function w(t,e){this.ownerDocument=t.ownerDocument,this.namespaceURI=t.namespaceURI,this._next=null,this._parent=t,this.__data__=e}w.prototype={constructor:w,appendChild:function(t){return this._parent.insertBefore(t,this._next)},insertBefore:function(t,e){return this._parent.insertBefore(t,e)},querySelector:function(t){return this._parent.querySelector(t)},querySelectorAll:function(t){return this._parent.querySelectorAll(t)}};function G(t){return function(){return t}}function Ht(t,e,r,i,n,o){for(var f=0,l,u=e.length,s=o.length;f<s;++f)(l=e[f])?(l.__data__=o[f],i[f]=l):r[f]=new w(t,o[f]);for(;f<u;++f)(l=e[f])&&(n[f]=l)}function Ut(t,e,r,i,n,o,f){var l,u,s=new Map,c=e.length,h=o.length,m=new Array(c),p;for(l=0;l<c;++l)(u=e[l])&&(m[l]=p=f.call(u,u.__data__,l,e)+"",s.has(p)?n[l]=u:s.set(p,u));for(l=0;l<h;++l)p=f.call(t,o[l],l,o)+"",(u=s.get(p))?(i[l]=u,u.__data__=o[l],s.delete(p)):r[l]=new w(t,o[l]);for(l=0;l<c;++l)(u=e[l])&&s.get(m[l])===u&&(n[l]=u)}function Xt(t){return t.__data__}function J(t,e){if(!arguments.length)return Array.from(this,Xt);var r=e?Ut:Ht,i=this._parents,n=this._groups;typeof t!="function"&&(t=G(t));for(var o=n.length,f=new Array(o),l=new Array(o),u=new Array(o),s=0;s<o;++s){var c=i[s],h=n[s],m=h.length,p=zt(t.call(c,c&&c.__data__,s,i)),_=p.length,D=l[s]=new Array(_),I=f[s]=new Array(_),Rt=u[s]=new Array(m);r(c,h,D,I,Rt,p,e);for(var y=0,C=0,O,k;y<_;++y)if(O=D[y]){for(y>=C&&(C=y+1);!(k=I[C])&&++C<_;);O._next=k||null}}return f=new a(f,i),f._enter=l,f._exit=u,f}function zt(t){return typeof t=="object"&&"length"in t?t:Array.from(t)}function Q(){return new a(this._exit||this._groups.map(b),this._parents)}function W(t,e,r){var i=this.enter(),n=this,o=this.exit();return typeof t=="function"?(i=t(i),i&&(i=i.selection())):i=i.append(t+""),e!=null&&(n=e(n),n&&(n=n.selection())),r==null?o.remove():r(o),i&&n?i.merge(n).order():n}function Z(t){for(var e=t.selection?t.selection():t,r=this._groups,i=e._groups,n=r.length,o=i.length,f=Math.min(n,o),l=new Array(n),u=0;u<f;++u)for(var s=r[u],c=i[u],h=s.length,m=l[u]=new Array(h),p,_=0;_<h;++_)(p=s[_]||c[_])&&(m[_]=p);for(;u<n;++u)l[u]=r[u];return new a(l,this._parents)}function $(){for(var t=this._groups,e=-1,r=t.length;++e<r;)for(var i=t[e],n=i.length-1,o=i[n],f;--n>=0;)(f=i[n])&&(o&&f.compareDocumentPosition(o)^4&&o.parentNode.insertBefore(f,o),o=f);return this}function j(t){t||(t=Yt);function e(h,m){return h&&m?t(h.__data__,m.__data__):!h-!m}for(var r=this._groups,i=r.length,n=new Array(i),o=0;o<i;++o){for(var f=r[o],l=f.length,u=n[o]=new Array(l),s,c=0;c<l;++c)(s=f[c])&&(u[c]=s);u.sort(e)}return new a(n,this._parents).order()}function Yt(t,e){return t<e?-1:t>e?1:t>=e?0:NaN}function tt(){var t=arguments[0];return arguments[0]=this,t.apply(null,arguments),this}function et(){return Array.from(this)}function rt(){for(var t=this._groups,e=0,r=t.length;e<r;++e)for(var i=t[e],n=0,o=i.length;n<o;++n){var f=i[n];if(f)return f}return null}function nt(){let t=0;for(let e of this)++t;return t}function it(){return!this.node()}function ot(t){for(var e=this._groups,r=0,i=e.length;r<i;++r)for(var n=e[r],o=0,f=n.length,l;o<f;++o)(l=n[o])&&t.call(l,l.__data__,o,n);return this}function Kt(t){return function(){this.removeAttribute(t)}}function Gt(t){return function(){this.removeAttributeNS(t.space,t.local)}}function Jt(t,e){return function(){this.setAttribute(t,e)}}function Qt(t,e){return function(){this.setAttributeNS(t.space,t.local,e)}}function Wt(t,e){return function(){var r=e.apply(this,arguments);r==null?this.removeAttribute(t):this.setAttribute(t,r)}}function Zt(t,e){return function(){var r=e.apply(this,arguments);r==null?this.removeAttributeNS(t.space,t.local):this.setAttributeNS(t.space,t.local,r)}}function lt(t,e){var r=x(t);if(arguments.length<2){var i=this.node();return r.local?i.getAttributeNS(r.space,r.local):i.getAttribute(r)}return this.each((e==null?r.local?Gt:Kt:typeof e=="function"?r.local?Zt:Wt:r.local?Qt:Jt)(r,e))}function A(t){return t.ownerDocument&&t.ownerDocument.defaultView||t.document&&t||t.defaultView}function $t(t){return function(){this.style.removeProperty(t)}}function jt(t,e,r){return function(){this.style.setProperty(t,e,r)}}function te(t,e,r){return function(){var i=e.apply(this,arguments);i==null?this.style.removeProperty(t):this.style.setProperty(t,i,r)}}function ft(t,e,r){return arguments.length>1?this.each((e==null?$t:typeof e=="function"?te:jt)(t,e,r??"")):ut(this.node(),t)}function ut(t,e){return t.style.getPropertyValue(e)||A(t).getComputedStyle(t,null).getPropertyValue(e)}function ee(t){return function(){delete this[t]}}function re(t,e){return function(){this[t]=e}}function ne(t,e){return function(){var r=e.apply(this,arguments);r==null?delete this[t]:this[t]=r}}function st(t,e){return arguments.length>1?this.each((e==null?ee:typeof e=="function"?ne:re)(t,e)):this.node()[t]}function ct(t){return t.trim().split(/^|\s+/)}function B(t){return t.classList||new at(t)}function at(t){this._node=t,this._names=ct(t.getAttribute("class")||"")}at.prototype={add:function(t){var e=this._names.indexOf(t);e<0&&(this._names.push(t),this._node.setAttribute("class",this._names.join(" ")))},remove:function(t){var e=this._names.indexOf(t);e>=0&&(this._names.splice(e,1),this._node.setAttribute("class",this._names.join(" ")))},contains:function(t){return this._names.indexOf(t)>=0}};function pt(t,e){for(var r=B(t),i=-1,n=e.length;++i<n;)r.add(e[i])}function ht(t,e){for(var r=B(t),i=-1,n=e.length;++i<n;)r.remove(e[i])}function ie(t){return function(){pt(this,t)}}function oe(t){return function(){ht(this,t)}}function le(t,e){return function(){(e.apply(this,arguments)?pt:ht)(this,t)}}function mt(t,e){var r=ct(t+"");if(arguments.length<2){for(var i=B(this.node()),n=-1,o=r.length;++n<o;)if(!i.contains(r[n]))return!1;return!0}return this.each((typeof e=="function"?le:e?ie:oe)(r,e))}function fe(){this.textContent=""}function ue(t){return function(){this.textContent=t}}function se(t){return function(){var e=t.apply(this,arguments);this.textContent=e??""}}function _t(t){return arguments.length?this.each(t==null?fe:(typeof t=="function"?se:ue)(t)):this.node().textContent}function ce(){this.innerHTML=""}function ae(t){return function(){this.innerHTML=t}}function pe(t){return function(){var e=t.apply(this,arguments);this.innerHTML=e??""}}function dt(t){return arguments.length?this.each(t==null?ce:(typeof t=="function"?pe:ae)(t)):this.node().innerHTML}function he(){this.nextSibling&&this.parentNode.appendChild(this)}function yt(){return this.each(he)}function me(){this.previousSibling&&this.parentNode.insertBefore(this,this.parentNode.firstChild)}function xt(){return this.each(me)}function gt(t){var e=typeof t=="function"?t:d(t);return this.select(function(){return this.appendChild(e.apply(this,arguments))})}function _e(){return null}function vt(t,e){var r=typeof t=="function"?t:d(t),i=e==null?_e:typeof e=="function"?e:g(e);return this.select(function(){return this.insertBefore(r.apply(this,arguments),i.apply(this,arguments)||null)})}function de(){var t=this.parentNode;t&&t.removeChild(this)}function wt(){return this.each(de)}function ye(){var t=this.cloneNode(!1),e=this.parentNode;return e?e.insertBefore(t,this.nextSibling):t}function xe(){var t=this.cloneNode(!0),e=this.parentNode;return e?e.insertBefore(t,this.nextSibling):t}function At(t){return this.select(t?xe:ye)}function St(t){return arguments.length?this.property("__data__",t):this.node().__data__}function ge(t){return function(e){t.call(this,e,this.__data__)}}function ve(t){return t.trim().split(/^|\s+/).map(function(e){var r="",i=e.indexOf(".");return i>=0&&(r=e.slice(i+1),e=e.slice(0,i)),{type:e,name:r}})}function we(t){return function(){var e=this.__on;if(e){for(var r=0,i=-1,n=e.length,o;r<n;++r)o=e[r],(!t.type||o.type===t.type)&&o.name===t.name?this.removeEventListener(o.type,o.listener,o.options):e[++i]=o;++i?e.length=i:delete this.__on}}}function Ae(t,e,r){return function(){var i=this.__on,n,o=ge(e);if(i){for(var f=0,l=i.length;f<l;++f)if((n=i[f]).type===t.type&&n.name===t.name){this.removeEventListener(n.type,n.listener,n.options),this.addEventListener(n.type,n.listener=o,n.options=r),n.value=e;return}}this.addEventListener(t.type,o,r),n={type:t.type,name:t.name,value:e,listener:o,options:r},i?i.push(n):this.__on=[n]}}function Ct(t,e,r){var i=ve(t+""),n,o=i.length,f;if(arguments.length<2){var l=this.node().__on;if(l){for(var u=0,s=l.length,c;u<s;++u)for(n=0,c=l[u];n<o;++n)if((f=i[n]).type===c.type&&f.name===c.name)return c.value}return}for(l=e?Ae:we,n=0;n<o;++n)this.each(l(i[n],e,r));return this}function Et(t,e,r){var i=A(t),n=i.CustomEvent;typeof n=="function"?n=new n(e,r):(n=i.document.createEvent("Event"),r?(n.initEvent(e,r.bubbles,r.cancelable),n.detail=r.detail):n.initEvent(e,!1,!1)),t.dispatchEvent(n)}function Se(t,e){return function(){return Et(this,t,e)}}function Ce(t,e){return function(){return Et(this,t,e.apply(this,arguments))}}function Nt(t,e){return this.each((typeof e=="function"?Ce:Se)(t,e))}function*Lt(){for(var t=this._groups,e=0,r=t.length;e<r;++e)for(var i=t[e],n=0,o=i.length,f;n<o;++n)(f=i[n])&&(yield f)}var S=[null];function a(t,e){this._groups=t,this._parents=e}function bt(){return new a([[document.documentElement]],S)}function Ee(){return this}a.prototype=bt.prototype={constructor:a,select:H,selectAll:U,selectChild:X,selectChildren:z,filter:Y,data:J,enter:K,exit:Q,join:W,merge:Z,selection:Ee,order:$,sort:j,call:tt,nodes:et,node:rt,size:nt,empty:it,each:ot,attr:lt,style:ft,property:st,classed:mt,text:_t,html:dt,raise:yt,lower:xt,append:gt,insert:vt,remove:wt,clone:At,datum:St,on:Ct,dispatch:Nt,[Symbol.iterator]:Lt};var Ne=bt;function M(t){return typeof t=="string"?new a([[document.querySelector(t)]],[document.documentElement]):new a([[t]],S)}function Le(t){return M(d(t).call(document.documentElement))}var be=0;function P(){return new T}function T(){this._="@"+(++be).toString(36)}T.prototype=P.prototype={constructor:T,get:function(t){for(var e=this._;!(e in t);)if(!(t=t.parentNode))return;return t[e]},set:function(t,e){return t[this._]=e},remove:function(t){return this._ in t&&delete t[this._]},toString:function(){return this._}};function R(t){let e;for(;e=t.sourceEvent;)t=e;return t}function q(t,e){if(t=R(t),e===void 0&&(e=t.currentTarget),e){var r=e.ownerSVGElement||e;if(r.createSVGPoint){var i=r.createSVGPoint();return i.x=t.clientX,i.y=t.clientY,i=i.matrixTransform(e.getScreenCTM().inverse()),[i.x,i.y]}if(e.getBoundingClientRect){var n=e.getBoundingClientRect();return[t.clientX-n.left-e.clientLeft,t.clientY-n.top-e.clientTop]}}return[t.pageX,t.pageY]}function Re(t,e){return t.target&&(t=R(t),e===void 0&&(e=t.currentTarget),t=t.touches||[t]),Array.from(t,r=>q(r,e))}function Ve(t){return typeof t=="string"?new a([document.querySelectorAll(t)],[document.documentElement]):new a([v(t)],S)}
    return {select:M};
    })(), (()=>{
    /* esm.sh - d3-drag@3.0.0 */
    var jt={value:()=>{}};function ut(){for(var t=0,e=arguments.length,r={},o;t<e;++t){if(!(o=arguments[t]+"")||o in r||/[\s.]/.test(o))throw new Error("illegal type: "+o);r[o]=[]}return new V(r)}function V(t){this._=t}function te(t,e){return t.trim().split(/^|\s+/).map(function(r){var o="",n=r.indexOf(".");if(n>=0&&(o=r.slice(n+1),r=r.slice(0,n)),r&&!e.hasOwnProperty(r))throw new Error("unknown type: "+r);return{type:r,name:o}})}V.prototype=ut.prototype={constructor:V,on:function(t,e){var r=this._,o=te(t+"",r),n,i=-1,u=o.length;if(arguments.length<2){for(;++i<u;)if((n=(t=o[i]).type)&&(n=ee(r[n],t.name)))return n;return}if(e!=null&&typeof e!="function")throw new Error("invalid callback: "+e);for(;++i<u;)if(n=(t=o[i]).type)r[n]=it(r[n],t.name,e);else if(e==null)for(n in r)r[n]=it(r[n],t.name,null);return this},copy:function(){var t={},e=this._;for(var r in e)t[r]=e[r].slice();return new V(t)},call:function(t,e){if((n=arguments.length-2)>0)for(var r=new Array(n),o=0,n,i;o<n;++o)r[o]=arguments[o+2];if(!this._.hasOwnProperty(t))throw new Error("unknown type: "+t);for(i=this._[t],o=0,n=i.length;o<n;++o)i[o].value.apply(e,r)},apply:function(t,e,r){if(!this._.hasOwnProperty(t))throw new Error("unknown type: "+t);for(var o=this._[t],n=0,i=o.length;n<i;++n)o[n].value.apply(e,r)}};function ee(t,e){for(var r=0,o=t.length,n;r<o;++r)if((n=t[r]).name===e)return n.value}function it(t,e,r){for(var o=0,n=t.length;o<n;++o)if(t[o].name===e){t[o]=jt,t=t.slice(0,o).concat(t.slice(o+1));break}return r!=null&&t.push({name:e,value:r}),t}var J=ut;var k="http://www.w3.org/1999/xhtml",Q={svg:"http://www.w3.org/2000/svg",xhtml:k,xlink:"http://www.w3.org/1999/xlink",xml:"http://www.w3.org/XML/1998/namespace",xmlns:"http://www.w3.org/2000/xmlns/"};function B(t){var e=t+="",r=e.indexOf(":");return r>=0&&(e=t.slice(0,r))!=="xmlns"&&(t=t.slice(r+1)),Q.hasOwnProperty(e)?{space:Q[e],local:t}:t}function re(t){return function(){var e=this.ownerDocument,r=this.namespaceURI;return r===k&&e.documentElement.namespaceURI===k?e.createElement(t):e.createElementNS(r,t)}}function ne(t){return function(){return this.ownerDocument.createElementNS(t.space,t.local)}}function O(t){var e=B(t);return(e.local?ne:re)(e)}function oe(){}function q(t){return t==null?oe:function(){return this.querySelector(t)}}function lt(t){typeof t!="function"&&(t=q(t));for(var e=this._groups,r=e.length,o=new Array(r),n=0;n<r;++n)for(var i=e[n],u=i.length,s=o[n]=new Array(u),a,f,c=0;c<u;++c)(a=i[c])&&(f=t.call(a,a.__data__,c,i))&&("__data__"in a&&(f.__data__=a.__data__),s[c]=f);return new m(o,this._parents)}function W(t){return t==null?[]:Array.isArray(t)?t:Array.from(t)}function ie(){return[]}function st(t){return t==null?ie:function(){return this.querySelectorAll(t)}}function ue(t){return function(){return W(t.apply(this,arguments))}}function at(t){typeof t=="function"?t=ue(t):t=st(t);for(var e=this._groups,r=e.length,o=[],n=[],i=0;i<r;++i)for(var u=e[i],s=u.length,a,f=0;f<s;++f)(a=u[f])&&(o.push(t.call(a,a.__data__,f,u)),n.push(a));return new m(o,n)}function ft(t){return function(){return this.matches(t)}}function I(t){return function(e){return e.matches(t)}}var le=Array.prototype.find;function se(t){return function(){return le.call(this.children,t)}}function ae(){return this.firstElementChild}function ct(t){return this.select(t==null?ae:se(typeof t=="function"?t:I(t)))}var fe=Array.prototype.filter;function ce(){return Array.from(this.children)}function he(t){return function(){return fe.call(this.children,t)}}function ht(t){return this.selectAll(t==null?ce:he(typeof t=="function"?t:I(t)))}function pt(t){typeof t!="function"&&(t=ft(t));for(var e=this._groups,r=e.length,o=new Array(r),n=0;n<r;++n)for(var i=e[n],u=i.length,s=o[n]=[],a,f=0;f<u;++f)(a=i[f])&&t.call(a,a.__data__,f,i)&&s.push(a);return new m(o,this._parents)}function U(t){return new Array(t.length)}function mt(){return new m(this._enter||this._groups.map(U),this._parents)}function P(t,e){this.ownerDocument=t.ownerDocument,this.namespaceURI=t.namespaceURI,this._next=null,this._parent=t,this.__data__=e}P.prototype={constructor:P,appendChild:function(t){return this._parent.insertBefore(t,this._next)},insertBefore:function(t,e){return this._parent.insertBefore(t,e)},querySelector:function(t){return this._parent.querySelector(t)},querySelectorAll:function(t){return this._parent.querySelectorAll(t)}};function dt(t){return function(){return t}}function pe(t,e,r,o,n,i){for(var u=0,s,a=e.length,f=i.length;u<f;++u)(s=e[u])?(s.__data__=i[u],o[u]=s):r[u]=new P(t,i[u]);for(;u<a;++u)(s=e[u])&&(n[u]=s)}function me(t,e,r,o,n,i,u){var s,a,f=new Map,c=e.length,_=i.length,h=new Array(c),y;for(s=0;s<c;++s)(a=e[s])&&(h[s]=y=u.call(a,a.__data__,s,e)+"",f.has(y)?n[s]=a:f.set(y,a));for(s=0;s<_;++s)y=u.call(t,i[s],s,i)+"",(a=f.get(y))?(o[s]=a,a.__data__=i[s],f.delete(y)):r[s]=new P(t,i[s]);for(s=0;s<c;++s)(a=e[s])&&f.get(h[s])===a&&(n[s]=a)}function de(t){return t.__data__}function gt(t,e){if(!arguments.length)return Array.from(this,de);var r=e?me:pe,o=this._parents,n=this._groups;typeof t!="function"&&(t=dt(t));for(var i=n.length,u=new Array(i),s=new Array(i),a=new Array(i),f=0;f<i;++f){var c=o[f],_=n[f],h=_.length,y=ge(t.call(c,c&&c.__data__,f,o)),v=y.length,M=s[f]=new Array(v),F=u[f]=new Array(v),H=a[f]=new Array(h);r(c,_,M,F,H,y,e);for(var S=0,E=0,l,p;S<v;++S)if(l=M[S]){for(S>=E&&(E=S+1);!(p=F[E])&&++E<v;);l._next=p||null}}return u=new m(u,o),u._enter=s,u._exit=a,u}function ge(t){return typeof t=="object"&&"length"in t?t:Array.from(t)}function _t(){return new m(this._exit||this._groups.map(U),this._parents)}function yt(t,e,r){var o=this.enter(),n=this,i=this.exit();return typeof t=="function"?(o=t(o),o&&(o=o.selection())):o=o.append(t+""),e!=null&&(n=e(n),n&&(n=n.selection())),r==null?i.remove():r(i),o&&n?o.merge(n).order():n}function vt(t){for(var e=t.selection?t.selection():t,r=this._groups,o=e._groups,n=r.length,i=o.length,u=Math.min(n,i),s=new Array(n),a=0;a<u;++a)for(var f=r[a],c=o[a],_=f.length,h=s[a]=new Array(_),y,v=0;v<_;++v)(y=f[v]||c[v])&&(h[v]=y);for(;a<n;++a)s[a]=r[a];return new m(s,this._parents)}function xt(){for(var t=this._groups,e=-1,r=t.length;++e<r;)for(var o=t[e],n=o.length-1,i=o[n],u;--n>=0;)(u=o[n])&&(i&&u.compareDocumentPosition(i)^4&&i.parentNode.insertBefore(u,i),i=u);return this}function wt(t){t||(t=_e);function e(_,h){return _&&h?t(_.__data__,h.__data__):!_-!h}for(var r=this._groups,o=r.length,n=new Array(o),i=0;i<o;++i){for(var u=r[i],s=u.length,a=n[i]=new Array(s),f,c=0;c<s;++c)(f=u[c])&&(a[c]=f);a.sort(e)}return new m(n,this._parents).order()}function _e(t,e){return t<e?-1:t>e?1:t>=e?0:NaN}function At(){var t=arguments[0];return arguments[0]=this,t.apply(null,arguments),this}function bt(){return Array.from(this)}function St(){for(var t=this._groups,e=0,r=t.length;e<r;++e)for(var o=t[e],n=0,i=o.length;n<i;++n){var u=o[n];if(u)return u}return null}function Et(){let t=0;for(let e of this)++t;return t}function Ct(){return!this.node()}function Nt(t){for(var e=this._groups,r=0,o=e.length;r<o;++r)for(var n=e[r],i=0,u=n.length,s;i<u;++i)(s=n[i])&&t.call(s,s.__data__,i,n);return this}function ye(t){return function(){this.removeAttribute(t)}}function ve(t){return function(){this.removeAttributeNS(t.space,t.local)}}function xe(t,e){return function(){this.setAttribute(t,e)}}function we(t,e){return function(){this.setAttributeNS(t.space,t.local,e)}}function Ae(t,e){return function(){var r=e.apply(this,arguments);r==null?this.removeAttribute(t):this.setAttribute(t,r)}}function be(t,e){return function(){var r=e.apply(this,arguments);r==null?this.removeAttributeNS(t.space,t.local):this.setAttributeNS(t.space,t.local,r)}}function Tt(t,e){var r=B(t);if(arguments.length<2){var o=this.node();return r.local?o.getAttributeNS(r.space,r.local):o.getAttribute(r)}return this.each((e==null?r.local?ve:ye:typeof e=="function"?r.local?be:Ae:r.local?we:xe)(r,e))}function z(t){return t.ownerDocument&&t.ownerDocument.defaultView||t.document&&t||t.defaultView}function Se(t){return function(){this.style.removeProperty(t)}}function Ee(t,e,r){return function(){this.style.setProperty(t,e,r)}}function Ce(t,e,r){return function(){var o=e.apply(this,arguments);o==null?this.style.removeProperty(t):this.style.setProperty(t,o,r)}}function Pt(t,e,r){return arguments.length>1?this.each((e==null?Se:typeof e=="function"?Ce:Ee)(t,e,r??"")):Ne(this.node(),t)}function Ne(t,e){return t.style.getPropertyValue(e)||z(t).getComputedStyle(t,null).getPropertyValue(e)}function Te(t){return function(){delete this[t]}}function Pe(t,e){return function(){this[t]=e}}function De(t,e){return function(){var r=e.apply(this,arguments);r==null?delete this[t]:this[t]=r}}function Dt(t,e){return arguments.length>1?this.each((e==null?Te:typeof e=="function"?De:Pe)(t,e)):this.node()[t]}function Lt(t){return t.trim().split(/^|\s+/)}function Z(t){return t.classList||new Mt(t)}function Mt(t){this._node=t,this._names=Lt(t.getAttribute("class")||"")}Mt.prototype={add:function(t){var e=this._names.indexOf(t);e<0&&(this._names.push(t),this._node.setAttribute("class",this._names.join(" ")))},remove:function(t){var e=this._names.indexOf(t);e>=0&&(this._names.splice(e,1),this._node.setAttribute("class",this._names.join(" ")))},contains:function(t){return this._names.indexOf(t)>=0}};function Ft(t,e){for(var r=Z(t),o=-1,n=e.length;++o<n;)r.add(e[o])}function Rt(t,e){for(var r=Z(t),o=-1,n=e.length;++o<n;)r.remove(e[o])}function Le(t){return function(){Ft(this,t)}}function Me(t){return function(){Rt(this,t)}}function Fe(t,e){return function(){(e.apply(this,arguments)?Ft:Rt)(this,t)}}function Vt(t,e){var r=Lt(t+"");if(arguments.length<2){for(var o=Z(this.node()),n=-1,i=r.length;++n<i;)if(!o.contains(r[n]))return!1;return!0}return this.each((typeof e=="function"?Fe:e?Le:Me)(r,e))}function Re(){this.textContent=""}function Ve(t){return function(){this.textContent=t}}function ke(t){return function(){var e=t.apply(this,arguments);this.textContent=e??""}}function kt(t){return arguments.length?this.each(t==null?Re:(typeof t=="function"?ke:Ve)(t)):this.node().textContent}function Be(){this.innerHTML=""}function Oe(t){return function(){this.innerHTML=t}}function qe(t){return function(){var e=t.apply(this,arguments);this.innerHTML=e??""}}function Bt(t){return arguments.length?this.each(t==null?Be:(typeof t=="function"?qe:Oe)(t)):this.node().innerHTML}function Ie(){this.nextSibling&&this.parentNode.appendChild(this)}function Ot(){return this.each(Ie)}function Ue(){this.previousSibling&&this.parentNode.insertBefore(this,this.parentNode.firstChild)}function qt(){return this.each(Ue)}function It(t){var e=typeof t=="function"?t:O(t);return this.select(function(){return this.appendChild(e.apply(this,arguments))})}function ze(){return null}function Ut(t,e){var r=typeof t=="function"?t:O(t),o=e==null?ze:typeof e=="function"?e:q(e);return this.select(function(){return this.insertBefore(r.apply(this,arguments),o.apply(this,arguments)||null)})}function Xe(){var t=this.parentNode;t&&t.removeChild(this)}function zt(){return this.each(Xe)}function Ye(){var t=this.cloneNode(!1),e=this.parentNode;return e?e.insertBefore(t,this.nextSibling):t}function He(){var t=this.cloneNode(!0),e=this.parentNode;return e?e.insertBefore(t,this.nextSibling):t}function Xt(t){return this.select(t?He:Ye)}function Yt(t){return arguments.length?this.property("__data__",t):this.node().__data__}function Ke(t){return function(e){t.call(this,e,this.__data__)}}function Ge(t){return t.trim().split(/^|\s+/).map(function(e){var r="",o=e.indexOf(".");return o>=0&&(r=e.slice(o+1),e=e.slice(0,o)),{type:e,name:r}})}function Je(t){return function(){var e=this.__on;if(e){for(var r=0,o=-1,n=e.length,i;r<n;++r)i=e[r],(!t.type||i.type===t.type)&&i.name===t.name?this.removeEventListener(i.type,i.listener,i.options):e[++o]=i;++o?e.length=o:delete this.__on}}}function Qe(t,e,r){return function(){var o=this.__on,n,i=Ke(e);if(o){for(var u=0,s=o.length;u<s;++u)if((n=o[u]).type===t.type&&n.name===t.name){this.removeEventListener(n.type,n.listener,n.options),this.addEventListener(n.type,n.listener=i,n.options=r),n.value=e;return}}this.addEventListener(t.type,i,r),n={type:t.type,name:t.name,value:e,listener:i,options:r},o?o.push(n):this.__on=[n]}}function Ht(t,e,r){var o=Ge(t+""),n,i=o.length,u;if(arguments.length<2){var s=this.node().__on;if(s){for(var a=0,f=s.length,c;a<f;++a)for(n=0,c=s[a];n<i;++n)if((u=o[n]).type===c.type&&u.name===c.name)return c.value}return}for(s=e?Qe:Je,n=0;n<i;++n)this.each(s(o[n],e,r));return this}function Kt(t,e,r){var o=z(t),n=o.CustomEvent;typeof n=="function"?n=new n(e,r):(n=o.document.createEvent("Event"),r?(n.initEvent(e,r.bubbles,r.cancelable),n.detail=r.detail):n.initEvent(e,!1,!1)),t.dispatchEvent(n)}function We(t,e){return function(){return Kt(this,t,e)}}function Ze(t,e){return function(){return Kt(this,t,e.apply(this,arguments))}}function Gt(t,e){return this.each((typeof e=="function"?Ze:We)(t,e))}function*Jt(){for(var t=this._groups,e=0,r=t.length;e<r;++e)for(var o=t[e],n=0,i=o.length,u;n<i;++n)(u=o[n])&&(yield u)}var $=[null];function m(t,e){this._groups=t,this._parents=e}function $e(){return new m([[document.documentElement]],$)}function je(){return this}m.prototype=$e.prototype={constructor:m,select:lt,selectAll:at,selectChild:ct,selectChildren:ht,filter:pt,data:gt,enter:mt,exit:_t,join:yt,merge:vt,selection:je,order:xt,sort:wt,call:At,nodes:bt,node:St,size:Et,empty:Ct,each:Nt,attr:Tt,style:Pt,property:Dt,classed:Vt,text:kt,html:Bt,raise:Ot,lower:qt,append:It,insert:Ut,remove:zt,clone:Xt,datum:Yt,on:Ht,dispatch:Gt,[Symbol.iterator]:Jt};function C(t){return typeof t=="string"?new m([[document.querySelector(t)]],[document.documentElement]):new m([[t]],$)}function Qt(t){let e;for(;e=t.sourceEvent;)t=e;return t}function X(t,e){if(t=Qt(t),e===void 0&&(e=t.currentTarget),e){var r=e.ownerSVGElement||e;if(r.createSVGPoint){var o=r.createSVGPoint();return o.x=t.clientX,o.y=t.clientY,o=o.matrixTransform(e.getScreenCTM().inverse()),[o.x,o.y]}if(e.getBoundingClientRect){var n=e.getBoundingClientRect();return[t.clientX-n.left-e.clientLeft,t.clientY-n.top-e.clientTop]}}return[t.pageX,t.pageY]}var Wt={passive:!1},N={capture:!0,passive:!1};function Y(t){t.stopImmediatePropagation()}function b(t){t.preventDefault(),t.stopImmediatePropagation()}function j(t){var e=t.document.documentElement,r=C(t).on("dragstart.drag",b,N);"onselectstart"in e?r.on("selectstart.drag",b,N):(e.__noselect=e.style.MozUserSelect,e.style.MozUserSelect="none")}function tt(t,e){var r=t.document.documentElement,o=C(t).on("dragstart.drag",null);e&&(o.on("click.drag",b,N),setTimeout(function(){o.on("click.drag",null)},0)),"onselectstart"in r?o.on("selectstart.drag",null):(r.style.MozUserSelect=r.__noselect,delete r.__noselect)}var D=t=>()=>t;function L(t,{sourceEvent:e,subject:r,target:o,identifier:n,active:i,x:u,y:s,dx:a,dy:f,dispatch:c}){Object.defineProperties(this,{type:{value:t,enumerable:!0,configurable:!0},sourceEvent:{value:e,enumerable:!0,configurable:!0},subject:{value:r,enumerable:!0,configurable:!0},target:{value:o,enumerable:!0,configurable:!0},identifier:{value:n,enumerable:!0,configurable:!0},active:{value:i,enumerable:!0,configurable:!0},x:{value:u,enumerable:!0,configurable:!0},y:{value:s,enumerable:!0,configurable:!0},dx:{value:a,enumerable:!0,configurable:!0},dy:{value:f,enumerable:!0,configurable:!0},_:{value:c}})}L.prototype.on=function(){var t=this._.on.apply(this._,arguments);return t===this._?this:t};function tr(t){return!t.ctrlKey&&!t.button}function er(){return this.parentNode}function rr(t,e){return e??{x:t.x,y:t.y}}function nr(){return navigator.maxTouchPoints||"ontouchstart"in this}function or(){var t=tr,e=er,r=rr,o=nr,n={},i=J("start","drag","end"),u=0,s,a,f,c,_=0;function h(l){l.on("mousedown.drag",y).filter(o).on("touchstart.drag",F).on("touchmove.drag",H,Wt).on("touchend.drag touchcancel.drag",S).style("touch-action","none").style("-webkit-tap-highlight-color","rgba(0,0,0,0)")}function y(l,p){if(!(c||!t.call(this,l,p))){var d=E(this,e.call(this,l,p),l,p,"mouse");d&&(C(l.view).on("mousemove.drag",v,N).on("mouseup.drag",M,N),j(l.view),Y(l),f=!1,s=l.clientX,a=l.clientY,d("start",l))}}function v(l){if(b(l),!f){var p=l.clientX-s,d=l.clientY-a;f=p*p+d*d>_}n.mouse("drag",l)}function M(l){C(l.view).on("mousemove.drag mouseup.drag",null),tt(l.view,f),b(l),n.mouse("end",l)}function F(l,p){if(t.call(this,l,p)){var d=l.changedTouches,g=e.call(this,l,p),x=d.length,A,T;for(A=0;A<x;++A)(T=E(this,g,l,p,d[A].identifier,d[A]))&&(Y(l),T("start",l,d[A]))}}function H(l){var p=l.changedTouches,d=p.length,g,x;for(g=0;g<d;++g)(x=n[p[g].identifier])&&(b(l),x("drag",l,p[g]))}function S(l){var p=l.changedTouches,d=p.length,g,x;for(c&&clearTimeout(c),c=setTimeout(function(){c=null},500),g=0;g<d;++g)(x=n[p[g].identifier])&&(Y(l),x("end",l,p[g]))}function E(l,p,d,g,x,A){var T=i.copy(),w=X(A||d,p),et,rt,R;if((R=r.call(l,new L("beforestart",{sourceEvent:d,target:h,identifier:x,active:u,x:w[0],y:w[1],dx:0,dy:0,dispatch:T}),g))!=null)return et=R.x-w[0]||0,rt=R.y-w[1]||0,function Zt(K,nt,$t){var ot=w,G;switch(K){case"start":n[x]=Zt,G=u++;break;case"end":delete n[x],--u;case"drag":w=X($t||nt,p),G=u;break}T.call(K,l,new L(K,{sourceEvent:nt,subject:R,target:h,identifier:x,active:G,x:w[0]+et,y:w[1]+rt,dx:w[0]-ot[0],dy:w[1]-ot[1],dispatch:T}),g)}}return h.filter=function(l){return arguments.length?(t=typeof l=="function"?l:D(!!l),h):t},h.container=function(l){return arguments.length?(e=typeof l=="function"?l:D(l),h):e},h.subject=function(l){return arguments.length?(r=typeof l=="function"?l:D(l),h):r},h.touchable=function(l){return arguments.length?(o=typeof l=="function"?l:D(!!l),h):o},h.on=function(){var l=i.on.apply(i,arguments);return l===i?h:l},h.clickDistance=function(l){return arguments.length?(_=(l=+l)*l,h):Math.sqrt(_)},h}
    return {drag:or};
    })(), (()=>{
    /* esm.sh - d3-force@3.0.0 */
    function zt(t,n){var e,r=1;t==null&&(t=0),n==null&&(n=0);function i(){var f,l=e.length,a,c=0,o=0;for(f=0;f<l;++f)a=e[f],c+=a.x,o+=a.y;for(c=(c/l-t)*r,o=(o/l-n)*r,f=0;f<l;++f)a=e[f],a.x-=c,a.y-=o}return i.initialize=function(f){e=f},i.x=function(f){return arguments.length?(t=+f,i):t},i.y=function(f){return arguments.length?(n=+f,i):n},i.strength=function(f){return arguments.length?(r=+f,i):r},i}function Z(t){let n=+this._x.call(null,t),e=+this._y.call(null,t);return $(this.cover(n,e),n,e,t)}function $(t,n,e,r){if(isNaN(n)||isNaN(e))return t;var i,f=t._root,l={data:r},a=t._x0,c=t._y0,o=t._x1,g=t._y1,w,x,h,y,s,u,p,v;if(!f)return t._root=l,t;for(;f.length;)if((s=n>=(w=(a+o)/2))?a=w:o=w,(u=e>=(x=(c+g)/2))?c=x:g=x,i=f,!(f=f[p=u<<1|s]))return i[p]=l,t;if(h=+t._x.call(null,f.data),y=+t._y.call(null,f.data),n===h&&e===y)return l.next=f,i?i[p]=l:t._root=l,t;do i=i?i[p]=new Array(4):t._root=new Array(4),(s=n>=(w=(a+o)/2))?a=w:o=w,(u=e>=(x=(c+g)/2))?c=x:g=x;while((p=u<<1|s)===(v=(y>=x)<<1|h>=w));return i[v]=f,i[p]=l,t}function q(t){var n,e,r=t.length,i,f,l=new Array(r),a=new Array(r),c=1/0,o=1/0,g=-1/0,w=-1/0;for(e=0;e<r;++e)isNaN(i=+this._x.call(null,n=t[e]))||isNaN(f=+this._y.call(null,n))||(l[e]=i,a[e]=f,i<c&&(c=i),i>g&&(g=i),f<o&&(o=f),f>w&&(w=f));if(c>g||o>w)return this;for(this.cover(c,o).cover(g,w),e=0;e<r;++e)$(this,l[e],a[e],t[e]);return this}function tt(t,n){if(isNaN(t=+t)||isNaN(n=+n))return this;var e=this._x0,r=this._y0,i=this._x1,f=this._y1;if(isNaN(e))i=(e=Math.floor(t))+1,f=(r=Math.floor(n))+1;else{for(var l=i-e||1,a=this._root,c,o;e>t||t>=i||r>n||n>=f;)switch(o=(n<r)<<1|t<e,c=new Array(4),c[o]=a,a=c,l*=2,o){case 0:i=e+l,f=r+l;break;case 1:e=i-l,f=r+l;break;case 2:i=e+l,r=f-l;break;case 3:e=i-l,r=f-l;break}this._root&&this._root.length&&(this._root=a)}return this._x0=e,this._y0=r,this._x1=i,this._y1=f,this}function nt(){var t=[];return this.visit(function(n){if(!n.length)do t.push(n.data);while(n=n.next)}),t}function et(t){return arguments.length?this.cover(+t[0][0],+t[0][1]).cover(+t[1][0],+t[1][1]):isNaN(this._x0)?void 0:[[this._x0,this._y0],[this._x1,this._y1]]}function z(t,n,e,r,i){this.node=t,this.x0=n,this.y0=e,this.x1=r,this.y1=i}function rt(t,n,e){var r,i=this._x0,f=this._y0,l,a,c,o,g=this._x1,w=this._y1,x=[],h=this._root,y,s;for(h&&x.push(new z(h,i,f,g,w)),e==null?e=1/0:(i=t-e,f=n-e,g=t+e,w=n+e,e*=e);y=x.pop();)if(!(!(h=y.node)||(l=y.x0)>g||(a=y.y0)>w||(c=y.x1)<i||(o=y.y1)<f))if(h.length){var u=(l+c)/2,p=(a+o)/2;x.push(new z(h[3],u,p,c,o),new z(h[2],l,p,u,o),new z(h[1],u,a,c,p),new z(h[0],l,a,u,p)),(s=(n>=p)<<1|t>=u)&&(y=x[x.length-1],x[x.length-1]=x[x.length-1-s],x[x.length-1-s]=y)}else{var v=t-+this._x.call(null,h.data),_=n-+this._y.call(null,h.data),m=v*v+_*_;if(m<e){var N=Math.sqrt(e=m);i=t-N,f=n-N,g=t+N,w=n+N,r=h.data}}return r}function it(t){if(isNaN(g=+this._x.call(null,t))||isNaN(w=+this._y.call(null,t)))return this;var n,e=this._root,r,i,f,l=this._x0,a=this._y0,c=this._x1,o=this._y1,g,w,x,h,y,s,u,p;if(!e)return this;if(e.length)for(;;){if((y=g>=(x=(l+c)/2))?l=x:c=x,(s=w>=(h=(a+o)/2))?a=h:o=h,n=e,!(e=e[u=s<<1|y]))return this;if(!e.length)break;(n[u+1&3]||n[u+2&3]||n[u+3&3])&&(r=n,p=u)}for(;e.data!==t;)if(i=e,!(e=e.next))return this;return(f=e.next)&&delete e.next,i?(f?i.next=f:delete i.next,this):n?(f?n[u]=f:delete n[u],(e=n[0]||n[1]||n[2]||n[3])&&e===(n[3]||n[2]||n[1]||n[0])&&!e.length&&(r?r[p]=e:this._root=e),this):(this._root=f,this)}function ot(t){for(var n=0,e=t.length;n<e;++n)this.remove(t[n]);return this}function ft(){return this._root}function at(){var t=0;return this.visit(function(n){if(!n.length)do++t;while(n=n.next)}),t}function ut(t){var n=[],e,r=this._root,i,f,l,a,c;for(r&&n.push(new z(r,this._x0,this._y0,this._x1,this._y1));e=n.pop();)if(!t(r=e.node,f=e.x0,l=e.y0,a=e.x1,c=e.y1)&&r.length){var o=(f+a)/2,g=(l+c)/2;(i=r[3])&&n.push(new z(i,o,g,a,c)),(i=r[2])&&n.push(new z(i,f,g,o,c)),(i=r[1])&&n.push(new z(i,o,l,a,g)),(i=r[0])&&n.push(new z(i,f,l,o,g))}return this}function lt(t){var n=[],e=[],r;for(this._root&&n.push(new z(this._root,this._x0,this._y0,this._x1,this._y1));r=n.pop();){var i=r.node;if(i.length){var f,l=r.x0,a=r.y0,c=r.x1,o=r.y1,g=(l+c)/2,w=(a+o)/2;(f=i[0])&&n.push(new z(f,l,a,g,w)),(f=i[1])&&n.push(new z(f,g,a,c,w)),(f=i[2])&&n.push(new z(f,l,w,g,o)),(f=i[3])&&n.push(new z(f,g,w,c,o))}e.push(r)}for(;r=e.pop();)t(r.node,r.x0,r.y0,r.x1,r.y1);return this}function st(t){return t[0]}function ht(t){return arguments.length?(this._x=t,this):this._x}function ct(t){return t[1]}function pt(t){return arguments.length?(this._y=t,this):this._y}function S(t,n,e){var r=new J(n??st,e??ct,NaN,NaN,NaN,NaN);return t==null?r:r.addAll(t)}function J(t,n,e,r,i,f){this._x=t,this._y=n,this._x0=e,this._y0=r,this._x1=i,this._y1=f,this._root=void 0}function gt(t){for(var n={data:t.data},e=n;t=t.next;)e=e.next={data:t.data};return n}var j=S.prototype=J.prototype;j.copy=function(){var t=new J(this._x,this._y,this._x0,this._y0,this._x1,this._y1),n=this._root,e,r;if(!n)return t;if(!n.length)return t._root=gt(n),t;for(e=[{source:n,target:t._root=new Array(4)}];n=e.pop();)for(var i=0;i<4;++i)(r=n.source[i])&&(r.length?e.push({source:r,target:n.target[i]=new Array(4)}):n.target[i]=gt(r));return t};j.add=Z;j.addAll=q;j.cover=tt;j.data=nt;j.extent=et;j.find=rt;j.remove=it;j.removeAll=ot;j.root=ft;j.size=at;j.visit=ut;j.visitAfter=lt;j.x=ht;j.y=pt;function d(t){return function(){return t}}function D(t){return(t()-.5)*1e-6}function It(t){return t.x+t.vx}function jt(t){return t.y+t.vy}function Et(t){var n,e,r,i=1,f=1;typeof t!="function"&&(t=d(t==null?1:+t));function l(){for(var o,g=n.length,w,x,h,y,s,u,p=0;p<f;++p)for(w=S(n,It,jt).visitAfter(a),o=0;o<g;++o)x=n[o],s=e[x.index],u=s*s,h=x.x+x.vx,y=x.y+x.vy,w.visit(v);function v(_,m,N,I,E){var A=_.data,T=_.r,M=s+T;if(A){if(A.index>x.index){var F=h-A.x-A.vx,P=y-A.y-A.vy,b=F*F+P*P;b<M*M&&(F===0&&(F=D(r),b+=F*F),P===0&&(P=D(r),b+=P*P),b=(M-(b=Math.sqrt(b)))/b*i,x.vx+=(F*=b)*(M=(T*=T)/(u+T)),x.vy+=(P*=b)*M,A.vx-=F*(M=1-M),A.vy-=P*M)}return}return m>h+M||I<h-M||N>y+M||E<y-M}}function a(o){if(o.data)return o.r=e[o.data.index];for(var g=o.r=0;g<4;++g)o[g]&&o[g].r>o.r&&(o.r=o[g].r)}function c(){if(n){var o,g=n.length,w;for(e=new Array(g),o=0;o<g;++o)w=n[o],e[w.index]=+t(w,o,n)}}return l.initialize=function(o,g){n=o,r=g,c()},l.iterations=function(o){return arguments.length?(f=+o,l):f},l.strength=function(o){return arguments.length?(i=+o,l):i},l.radius=function(o){return arguments.length?(t=typeof o=="function"?o:d(+o),c(),l):t},l}function Tt(t){return t.index}function xt(t,n){var e=t.get(n);if(!e)throw new Error("node not found: "+n);return e}function Dt(t){var n=Tt,e=w,r,i=d(30),f,l,a,c,o,g=1;t==null&&(t=[]);function w(u){return 1/Math.min(a[u.source.index],a[u.target.index])}function x(u){for(var p=0,v=t.length;p<g;++p)for(var _=0,m,N,I,E,A,T,M;_<v;++_)m=t[_],N=m.source,I=m.target,E=I.x+I.vx-N.x-N.vx||D(o),A=I.y+I.vy-N.y-N.vy||D(o),T=Math.sqrt(E*E+A*A),T=(T-f[_])/T*u*r[_],E*=T,A*=T,I.vx-=E*(M=c[_]),I.vy-=A*M,N.vx+=E*(M=1-M),N.vy+=A*M}function h(){if(l){var u,p=l.length,v=t.length,_=new Map(l.map((N,I)=>[n(N,I,l),N])),m;for(u=0,a=new Array(p);u<v;++u)m=t[u],m.index=u,typeof m.source!="object"&&(m.source=xt(_,m.source)),typeof m.target!="object"&&(m.target=xt(_,m.target)),a[m.source.index]=(a[m.source.index]||0)+1,a[m.target.index]=(a[m.target.index]||0)+1;for(u=0,c=new Array(v);u<v;++u)m=t[u],c[u]=a[m.source.index]/(a[m.source.index]+a[m.target.index]);r=new Array(v),y(),f=new Array(v),s()}}function y(){if(l)for(var u=0,p=t.length;u<p;++u)r[u]=+e(t[u],u,t)}function s(){if(l)for(var u=0,p=t.length;u<p;++u)f[u]=+i(t[u],u,t)}return x.initialize=function(u,p){l=u,o=p,h()},x.links=function(u){return arguments.length?(t=u,h(),x):t},x.id=function(u){return arguments.length?(n=u,x):n},x.iterations=function(u){return arguments.length?(g=+u,x):g},x.strength=function(u){return arguments.length?(e=typeof u=="function"?u:d(+u),y(),x):e},x.distance=function(u){return arguments.length?(i=typeof u=="function"?u:d(+u),s(),x):i},x}var bt={value:()=>{}};function mt(){for(var t=0,n=arguments.length,e={},r;t<n;++t){if(!(r=arguments[t]+"")||r in e||/[\s.]/.test(r))throw new Error("illegal type: "+r);e[r]=[]}return new L(e)}function L(t){this._=t}function Ft(t,n){return t.trim().split(/^|\s+/).map(function(e){var r="",i=e.indexOf(".");if(i>=0&&(r=e.slice(i+1),e=e.slice(0,i)),e&&!n.hasOwnProperty(e))throw new Error("unknown type: "+e);return{type:e,name:r}})}L.prototype=mt.prototype={constructor:L,on:function(t,n){var e=this._,r=Ft(t+"",e),i,f=-1,l=r.length;if(arguments.length<2){for(;++f<l;)if((i=(t=r[f]).type)&&(i=Pt(e[i],t.name)))return i;return}if(n!=null&&typeof n!="function")throw new Error("invalid callback: "+n);for(;++f<l;)if(i=(t=r[f]).type)e[i]=vt(e[i],t.name,n);else if(n==null)for(i in e)e[i]=vt(e[i],t.name,null);return this},copy:function(){var t={},n=this._;for(var e in n)t[e]=n[e].slice();return new L(t)},call:function(t,n){if((i=arguments.length-2)>0)for(var e=new Array(i),r=0,i,f;r<i;++r)e[r]=arguments[r+2];if(!this._.hasOwnProperty(t))throw new Error("unknown type: "+t);for(f=this._[t],r=0,i=f.length;r<i;++r)f[r].value.apply(n,e)},apply:function(t,n,e){if(!this._.hasOwnProperty(t))throw new Error("unknown type: "+t);for(var r=this._[t],i=0,f=r.length;i<f;++i)r[i].value.apply(n,e)}};function Pt(t,n){for(var e=0,r=t.length,i;e<r;++e)if((i=t[e]).name===n)return i.value}function vt(t,n,e){for(var r=0,i=t.length;r<i;++r)if(t[r].name===n){t[r]=bt,t=t.slice(0,r).concat(t.slice(r+1));break}return e!=null&&t.push({name:n,value:e}),t}var K=mt;var Q=0,Y=0,X=0,wt=1e3,R,B,k=0,O=0,H=0,C=typeof performance=="object"&&performance.now?performance:Date,_t=typeof window=="object"&&window.requestAnimationFrame?window.requestAnimationFrame.bind(window):function(t){setTimeout(t,17)};function W(){return O||(_t(St),O=C.now()+H)}function St(){O=0}function U(){this._call=this._time=this._next=null}U.prototype=G.prototype={constructor:U,restart:function(t,n,e){if(typeof t!="function")throw new TypeError("callback is not a function");e=(e==null?W():+e)+(n==null?0:+n),!this._next&&B!==this&&(B?B._next=this:R=this,B=this),this._call=t,this._time=e,V()},stop:function(){this._call&&(this._call=null,this._time=1/0,V())}};function G(t,n,e){var r=new U;return r.restart(t,n,e),r}function dt(){W(),++Q;for(var t=R,n;t;)(n=O-t._time)>=0&&t._call.call(void 0,n),t=t._next;--Q}function yt(){O=(k=C.now())+H,Q=Y=0;try{dt()}finally{Q=0,Qt(),O=0}}function Ot(){var t=C.now(),n=t-k;n>wt&&(H-=n,k=t)}function Qt(){for(var t,n=R,e,r=1/0;n;)n._call?(r>n._time&&(r=n._time),t=n,n=n._next):(e=n._next,n._next=null,n=t?t._next=e:R=e);B=t,V(r)}function V(t){if(!Q){Y&&(Y=clearTimeout(Y));var n=t-O;n>24?(t<1/0&&(Y=setTimeout(yt,t-C.now()-H)),X&&(X=clearInterval(X))):(X||(k=C.now(),X=setInterval(Ot,wt)),Q=1,_t(yt))}}function Nt(){let t=1;return()=>(t=(1664525*t+1013904223)%4294967296)/4294967296}function At(t){return t.x}function Mt(t){return t.y}var Xt=10,Yt=Math.PI*(3-Math.sqrt(5));function Bt(t){var n,e=1,r=.001,i=1-Math.pow(r,1/300),f=0,l=.6,a=new Map,c=G(w),o=K("tick","end"),g=Nt();t==null&&(t=[]);function w(){x(),o.call("tick",n),e<r&&(c.stop(),o.call("end",n))}function x(s){var u,p=t.length,v;s===void 0&&(s=1);for(var _=0;_<s;++_)for(e+=(f-e)*i,a.forEach(function(m){m(e)}),u=0;u<p;++u)v=t[u],v.fx==null?v.x+=v.vx*=l:(v.x=v.fx,v.vx=0),v.fy==null?v.y+=v.vy*=l:(v.y=v.fy,v.vy=0);return n}function h(){for(var s=0,u=t.length,p;s<u;++s){if(p=t[s],p.index=s,p.fx!=null&&(p.x=p.fx),p.fy!=null&&(p.y=p.fy),isNaN(p.x)||isNaN(p.y)){var v=Xt*Math.sqrt(.5+s),_=s*Yt;p.x=v*Math.cos(_),p.y=v*Math.sin(_)}(isNaN(p.vx)||isNaN(p.vy))&&(p.vx=p.vy=0)}}function y(s){return s.initialize&&s.initialize(t,g),s}return h(),n={tick:x,restart:function(){return c.restart(w),n},stop:function(){return c.stop(),n},nodes:function(s){return arguments.length?(t=s,h(),a.forEach(y),n):t},alpha:function(s){return arguments.length?(e=+s,n):e},alphaMin:function(s){return arguments.length?(r=+s,n):r},alphaDecay:function(s){return arguments.length?(i=+s,n):+i},alphaTarget:function(s){return arguments.length?(f=+s,n):f},velocityDecay:function(s){return arguments.length?(l=1-s,n):1-l},randomSource:function(s){return arguments.length?(g=s,a.forEach(y),n):g},force:function(s,u){return arguments.length>1?(u==null?a.delete(s):a.set(s,y(u)),n):a.get(s)},find:function(s,u,p){var v=0,_=t.length,m,N,I,E,A;for(p==null?p=1/0:p*=p,v=0;v<_;++v)E=t[v],m=s-E.x,N=u-E.y,I=m*m+N*N,I<p&&(A=E,p=I);return A},on:function(s,u){return arguments.length>1?(o.on(s,u),n):o.on(s)}}}function Ct(){var t,n,e,r,i=d(-30),f,l=1,a=1/0,c=.81;function o(h){var y,s=t.length,u=S(t,At,Mt).visitAfter(w);for(r=h,y=0;y<s;++y)n=t[y],u.visit(x)}function g(){if(t){var h,y=t.length,s;for(f=new Array(y),h=0;h<y;++h)s=t[h],f[s.index]=+i(s,h,t)}}function w(h){var y=0,s,u,p=0,v,_,m;if(h.length){for(v=_=m=0;m<4;++m)(s=h[m])&&(u=Math.abs(s.value))&&(y+=s.value,p+=u,v+=u*s.x,_+=u*s.y);h.x=v/p,h.y=_/p}else{s=h,s.x=s.data.x,s.y=s.data.y;do y+=f[s.data.index];while(s=s.next)}h.value=y}function x(h,y,s,u){if(!h.value)return!0;var p=h.x-n.x,v=h.y-n.y,_=u-y,m=p*p+v*v;if(_*_/c<m)return m<a&&(p===0&&(p=D(e),m+=p*p),v===0&&(v=D(e),m+=v*v),m<l&&(m=Math.sqrt(l*m)),n.vx+=p*h.value*r/m,n.vy+=v*h.value*r/m),!0;if(h.length||m>=a)return;(h.data!==n||h.next)&&(p===0&&(p=D(e),m+=p*p),v===0&&(v=D(e),m+=v*v),m<l&&(m=Math.sqrt(l*m)));do h.data!==n&&(_=f[h.data.index]*r/m,n.vx+=p*_,n.vy+=v*_);while(h=h.next)}return o.initialize=function(h,y){t=h,e=y,g()},o.strength=function(h){return arguments.length?(i=typeof h=="function"?h:d(+h),g(),o):i},o.distanceMin=function(h){return arguments.length?(l=h*h,o):Math.sqrt(l)},o.distanceMax=function(h){return arguments.length?(a=h*h,o):Math.sqrt(a)},o.theta=function(h){return arguments.length?(c=h*h,o):Math.sqrt(c)},o}function Lt(t,n,e){var r,i=d(.1),f,l;typeof t!="function"&&(t=d(+t)),n==null&&(n=0),e==null&&(e=0);function a(o){for(var g=0,w=r.length;g<w;++g){var x=r[g],h=x.x-n||1e-6,y=x.y-e||1e-6,s=Math.sqrt(h*h+y*y),u=(l[g]-s)*f[g]*o/s;x.vx+=h*u,x.vy+=y*u}}function c(){if(r){var o,g=r.length;for(f=new Array(g),l=new Array(g),o=0;o<g;++o)l[o]=+t(r[o],o,r),f[o]=isNaN(l[o])?0:+i(r[o],o,r)}}return a.initialize=function(o){r=o,c()},a.strength=function(o){return arguments.length?(i=typeof o=="function"?o:d(+o),c(),a):i},a.radius=function(o){return arguments.length?(t=typeof o=="function"?o:d(+o),c(),a):t},a.x=function(o){return arguments.length?(n=+o,a):n},a.y=function(o){return arguments.length?(e=+o,a):e},a}function Rt(t){var n=d(.1),e,r,i;typeof t!="function"&&(t=d(t==null?0:+t));function f(a){for(var c=0,o=e.length,g;c<o;++c)g=e[c],g.vx+=(i[c]-g.x)*r[c]*a}function l(){if(e){var a,c=e.length;for(r=new Array(c),i=new Array(c),a=0;a<c;++a)r[a]=isNaN(i[a]=+t(e[a],a,e))?0:+n(e[a],a,e)}}return f.initialize=function(a){e=a,l()},f.strength=function(a){return arguments.length?(n=typeof a=="function"?a:d(+a),l(),f):n},f.x=function(a){return arguments.length?(t=typeof a=="function"?a:d(+a),l(),f):t},f}function kt(t){var n=d(.1),e,r,i;typeof t!="function"&&(t=d(t==null?0:+t));function f(a){for(var c=0,o=e.length,g;c<o;++c)g=e[c],g.vy+=(i[c]-g.y)*r[c]*a}function l(){if(e){var a,c=e.length;for(r=new Array(c),i=new Array(c),a=0;a<c;++a)r[a]=isNaN(i[a]=+t(e[a],a,e))?0:+n(e[a],a,e)}}return f.initialize=function(a){e=a,l()},f.strength=function(a){return arguments.length?(n=typeof a=="function"?a:d(+a),l(),f):n},f.y=function(a){return arguments.length?(t=typeof a=="function"?a:d(+a),l(),f):t},f}
    return {forceSimulation:Bt,forceLink:Dt,forceManyBody:Ct,forceCenter:zt,forceCollide:Et};
    })());
    const rough = (()=>{
    /* esm.sh - roughjs@4.6.6 */
    function Y(a,t,s){if(a&&a.length){let[e,n]=t,o=Math.PI/180*s,r=Math.cos(o),h=Math.sin(o);for(let i of a){let[l,c]=i;i[0]=(l-e)*r-(c-n)*h+e,i[1]=(l-e)*h+(c-n)*r+n}}}function zt(a,t){return a[0]===t[0]&&a[1]===t[1]}function Wt(a,t,s,e=1){let n=s,o=Math.max(t,.1),r=a[0]&&a[0][0]&&typeof a[0][0]=="number"?[a]:a,h=[0,0];if(n)for(let l of r)Y(l,h,n);let i=(function(l,c,d){let p=[];for(let M of l){let m=[...M];zt(m[0],m[m.length-1])||m.push([m[0][0],m[0][1]]),m.length>2&&p.push(m)}let u=[];c=Math.max(c,.1);let f=[];for(let M of p)for(let m=0;m<M.length-1;m++){let P=M[m],x=M[m+1];if(P[1]!==x[1]){let w=Math.min(P[1],x[1]);f.push({ymin:w,ymax:Math.max(P[1],x[1]),x:w===P[1]?P[0]:x[0],islope:(x[0]-P[0])/(x[1]-P[1])})}}if(f.sort(((M,m)=>M.ymin<m.ymin?-1:M.ymin>m.ymin?1:M.x<m.x?-1:M.x>m.x?1:M.ymax===m.ymax?0:(M.ymax-m.ymax)/Math.abs(M.ymax-m.ymax))),!f.length)return u;let g=[],k=f[0].ymin,b=0;for(;g.length||f.length;){if(f.length){let M=-1;for(let m=0;m<f.length&&!(f[m].ymin>k);m++)M=m;f.splice(0,M+1).forEach((m=>{g.push({s:k,edge:m})}))}if(g=g.filter((M=>!(M.edge.ymax<=k))),g.sort(((M,m)=>M.edge.x===m.edge.x?0:(M.edge.x-m.edge.x)/Math.abs(M.edge.x-m.edge.x))),(d!==1||b%c==0)&&g.length>1)for(let M=0;M<g.length;M+=2){let m=M+1;if(m>=g.length)break;let P=g[M].edge,x=g[m].edge;u.push([[Math.round(P.x),k],[Math.round(x.x),k]])}k+=d,g.forEach((M=>{M.edge.x=M.edge.x+d*M.edge.islope})),b++}return u})(r,o,e);if(n){for(let l of r)Y(l,h,-n);(function(l,c,d){let p=[];l.forEach((u=>p.push(...u))),Y(p,c,d)})(i,h,-n)}return i}function F(a,t){var s;let e=t.hachureAngle+90,n=t.hachureGap;n<0&&(n=4*t.strokeWidth),n=Math.round(Math.max(n,.1));let o=1;return t.roughness>=1&&(((s=t.randomizer)===null||s===void 0?void 0:s.next())||Math.random())>.7&&(o=n),Wt(a,n,e,o||1)}var q=class{constructor(t){this.helper=t}fillPolygons(t,s){return this._fillPolygons(t,s)}_fillPolygons(t,s){let e=F(t,s);return{type:"fillSketch",ops:this.renderLines(e,s)}}renderLines(t,s){let e=[];for(let n of t)e.push(...this.helper.doubleLineOps(n[0][0],n[0][1],n[1][0],n[1][1],s));return e}};function X(a){let t=a[0],s=a[1];return Math.sqrt(Math.pow(t[0]-s[0],2)+Math.pow(t[1]-s[1],2))}var at=class extends q{fillPolygons(t,s){let e=s.hachureGap;e<0&&(e=4*s.strokeWidth),e=Math.max(e,.1);let n=F(t,Object.assign({},s,{hachureGap:e})),o=Math.PI/180*s.hachureAngle,r=[],h=.5*e*Math.cos(o),i=.5*e*Math.sin(o);for(let[l,c]of n)X([l,c])&&r.push([[l[0]-h,l[1]+i],[...c]],[[l[0]+h,l[1]-i],[...c]]);return{type:"fillSketch",ops:this.renderLines(r,s)}}},ot=class extends q{fillPolygons(t,s){let e=this._fillPolygons(t,s),n=Object.assign({},s,{hachureAngle:s.hachureAngle+90}),o=this._fillPolygons(t,n);return e.ops=e.ops.concat(o.ops),e}},ht=class{constructor(t){this.helper=t}fillPolygons(t,s){let e=F(t,s=Object.assign({},s,{hachureAngle:0}));return this.dotsOnLines(e,s)}dotsOnLines(t,s){let e=[],n=s.hachureGap;n<0&&(n=4*s.strokeWidth),n=Math.max(n,.1);let o=s.fillWeight;o<0&&(o=s.strokeWidth/2);let r=n/4;for(let h of t){let i=X(h),l=i/n,c=Math.ceil(l)-1,d=i-c*n,p=(h[0][0]+h[1][0])/2-n/4,u=Math.min(h[0][1],h[1][1]);for(let f=0;f<c;f++){let g=u+d+f*n,k=p-r+2*Math.random()*r,b=g-r+2*Math.random()*r,M=this.helper.ellipse(k,b,o,o,s);e.push(...M.ops)}}return{type:"fillSketch",ops:e}}},rt=class{constructor(t){this.helper=t}fillPolygons(t,s){let e=F(t,s);return{type:"fillSketch",ops:this.dashedLine(e,s)}}dashedLine(t,s){let e=s.dashOffset<0?s.hachureGap<0?4*s.strokeWidth:s.hachureGap:s.dashOffset,n=s.dashGap<0?s.hachureGap<0?4*s.strokeWidth:s.hachureGap:s.dashGap,o=[];return t.forEach((r=>{let h=X(r),i=Math.floor(h/(e+n)),l=(h+n-i*(e+n))/2,c=r[0],d=r[1];c[0]>d[0]&&(c=r[1],d=r[0]);let p=Math.atan((d[1]-c[1])/(d[0]-c[0]));for(let u=0;u<i;u++){let f=u*(e+n),g=f+e,k=[c[0]+f*Math.cos(p)+l*Math.cos(p),c[1]+f*Math.sin(p)+l*Math.sin(p)],b=[c[0]+g*Math.cos(p)+l*Math.cos(p),c[1]+g*Math.sin(p)+l*Math.sin(p)];o.push(...this.helper.doubleLineOps(k[0],k[1],b[0],b[1],s))}})),o}},it=class{constructor(t){this.helper=t}fillPolygons(t,s){let e=s.hachureGap<0?4*s.strokeWidth:s.hachureGap,n=s.zigzagOffset<0?e:s.zigzagOffset,o=F(t,s=Object.assign({},s,{hachureGap:e+n}));return{type:"fillSketch",ops:this.zigzagLines(o,n,s)}}zigzagLines(t,s,e){let n=[];return t.forEach((o=>{let r=X(o),h=Math.round(r/(2*s)),i=o[0],l=o[1];i[0]>l[0]&&(i=o[1],l=o[0]);let c=Math.atan((l[1]-i[1])/(l[0]-i[0]));for(let d=0;d<h;d++){let p=2*d*s,u=2*(d+1)*s,f=Math.sqrt(2*Math.pow(s,2)),g=[i[0]+p*Math.cos(c),i[1]+p*Math.sin(c)],k=[i[0]+u*Math.cos(c),i[1]+u*Math.sin(c)],b=[g[0]+f*Math.cos(c+Math.PI/4),g[1]+f*Math.sin(c+Math.PI/4)];n.push(...this.helper.doubleLineOps(g[0],g[1],b[0],b[1],e),...this.helper.doubleLineOps(b[0],b[1],k[0],k[1],e))}})),n}},S={},ct=class{constructor(t){this.seed=t}next(){return this.seed?(2**31-1&(this.seed=Math.imul(48271,this.seed)))/2**31:Math.random()}},Et=0,tt=1,bt=2,Z={A:7,a:7,C:6,c:6,H:1,h:1,L:2,l:2,M:2,m:2,Q:4,q:4,S:4,s:4,T:2,t:2,V:1,v:1,Z:0,z:0};function et(a,t){return a.type===t}function gt(a){let t=[],s=(function(r){let h=new Array;for(;r!=="";)if(r.match(/^([ \t\r\n,]+)/))r=r.substr(RegExp.$1.length);else if(r.match(/^([aAcChHlLmMqQsStTvVzZ])/))h[h.length]={type:Et,text:RegExp.$1},r=r.substr(RegExp.$1.length);else{if(!r.match(/^(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)/))return[];h[h.length]={type:tt,text:`${parseFloat(RegExp.$1)}`},r=r.substr(RegExp.$1.length)}return h[h.length]={type:bt,text:""},h})(a),e="BOD",n=0,o=s[n];for(;!et(o,bt);){let r=0,h=[];if(e==="BOD"){if(o.text!=="M"&&o.text!=="m")return gt("M0,0"+a);n++,r=Z[o.text],e=o.text}else et(o,tt)?r=Z[e]:(n++,r=Z[o.text],e=o.text);if(!(n+r<s.length))throw new Error("Path data ended short");for(let i=n;i<n+r;i++){let l=s[i];if(!et(l,tt))throw new Error("Param not a number: "+e+","+l.text);h[h.length]=+l.text}if(typeof Z[e]!="number")throw new Error("Bad segment: "+e);{let i={key:e,data:h};t.push(i),n+=r,o=s[n],e==="M"&&(e="L"),e==="m"&&(e="l")}}return t}function Ot(a){let t=0,s=0,e=0,n=0,o=[];for(let{key:r,data:h}of a)switch(r){case"M":o.push({key:"M",data:[...h]}),[t,s]=h,[e,n]=h;break;case"m":t+=h[0],s+=h[1],o.push({key:"M",data:[t,s]}),e=t,n=s;break;case"L":o.push({key:"L",data:[...h]}),[t,s]=h;break;case"l":t+=h[0],s+=h[1],o.push({key:"L",data:[t,s]});break;case"C":o.push({key:"C",data:[...h]}),t=h[4],s=h[5];break;case"c":{let i=h.map(((l,c)=>c%2?l+s:l+t));o.push({key:"C",data:i}),t=i[4],s=i[5];break}case"Q":o.push({key:"Q",data:[...h]}),t=h[2],s=h[3];break;case"q":{let i=h.map(((l,c)=>c%2?l+s:l+t));o.push({key:"Q",data:i}),t=i[2],s=i[3];break}case"A":o.push({key:"A",data:[...h]}),t=h[5],s=h[6];break;case"a":t+=h[5],s+=h[6],o.push({key:"A",data:[h[0],h[1],h[2],h[3],h[4],t,s]});break;case"H":o.push({key:"H",data:[...h]}),t=h[0];break;case"h":t+=h[0],o.push({key:"H",data:[t]});break;case"V":o.push({key:"V",data:[...h]}),s=h[0];break;case"v":s+=h[0],o.push({key:"V",data:[s]});break;case"S":o.push({key:"S",data:[...h]}),t=h[2],s=h[3];break;case"s":{let i=h.map(((l,c)=>c%2?l+s:l+t));o.push({key:"S",data:i}),t=i[2],s=i[3];break}case"T":o.push({key:"T",data:[...h]}),t=h[0],s=h[1];break;case"t":t+=h[0],s+=h[1],o.push({key:"T",data:[t,s]});break;case"Z":case"z":o.push({key:"Z",data:[]}),t=e,s=n}return o}function Lt(a){let t=[],s="",e=0,n=0,o=0,r=0,h=0,i=0;for(let{key:l,data:c}of a){switch(l){case"M":t.push({key:"M",data:[...c]}),[e,n]=c,[o,r]=c;break;case"C":t.push({key:"C",data:[...c]}),e=c[4],n=c[5],h=c[2],i=c[3];break;case"L":t.push({key:"L",data:[...c]}),[e,n]=c;break;case"H":e=c[0],t.push({key:"L",data:[e,n]});break;case"V":n=c[0],t.push({key:"L",data:[e,n]});break;case"S":{let d=0,p=0;s==="C"||s==="S"?(d=e+(e-h),p=n+(n-i)):(d=e,p=n),t.push({key:"C",data:[d,p,...c]}),h=c[0],i=c[1],e=c[2],n=c[3];break}case"T":{let[d,p]=c,u=0,f=0;s==="Q"||s==="T"?(u=e+(e-h),f=n+(n-i)):(u=e,f=n);let g=e+2*(u-e)/3,k=n+2*(f-n)/3,b=d+2*(u-d)/3,M=p+2*(f-p)/3;t.push({key:"C",data:[g,k,b,M,d,p]}),h=u,i=f,e=d,n=p;break}case"Q":{let[d,p,u,f]=c,g=e+2*(d-e)/3,k=n+2*(p-n)/3,b=u+2*(d-u)/3,M=f+2*(p-f)/3;t.push({key:"C",data:[g,k,b,M,u,f]}),h=d,i=p,e=u,n=f;break}case"A":{let d=Math.abs(c[0]),p=Math.abs(c[1]),u=c[2],f=c[3],g=c[4],k=c[5],b=c[6];d===0||p===0?(t.push({key:"C",data:[e,n,k,b,k,b]}),e=k,n=b):(e!==k||n!==b)&&(Tt(e,n,k,b,d,p,u,f,g).forEach((function(M){t.push({key:"C",data:M})})),e=k,n=b);break}case"Z":t.push({key:"Z",data:[]}),e=o,n=r}s=l}return t}function R(a,t,s){return[a*Math.cos(s)-t*Math.sin(s),a*Math.sin(s)+t*Math.cos(s)]}function Tt(a,t,s,e,n,o,r,h,i,l){let c=(d=r,Math.PI*d/180);var d;let p=[],u=0,f=0,g=0,k=0;if(l)[u,f,g,k]=l;else{[a,t]=R(a,t,-c),[s,e]=R(s,e,-c);let T=(a-s)/2,v=(t-e)/2,_=T*T/(n*n)+v*v/(o*o);_>1&&(_=Math.sqrt(_),n*=_,o*=_);let W=n*n,E=o*o,It=W*E-W*v*v-E*T*T,Ct=W*v*v+E*T*T,kt=(h===i?-1:1)*Math.sqrt(Math.abs(It/Ct));g=kt*n*v/o+(a+s)/2,k=kt*-o*T/n+(t+e)/2,u=Math.asin(parseFloat(((t-k)/o).toFixed(9))),f=Math.asin(parseFloat(((e-k)/o).toFixed(9))),a<g&&(u=Math.PI-u),s<g&&(f=Math.PI-f),u<0&&(u=2*Math.PI+u),f<0&&(f=2*Math.PI+f),i&&u>f&&(u-=2*Math.PI),!i&&f>u&&(f-=2*Math.PI)}let b=f-u;if(Math.abs(b)>120*Math.PI/180){let T=f,v=s,_=e;f=i&&f>u?u+120*Math.PI/180*1:u+120*Math.PI/180*-1,p=Tt(s=g+n*Math.cos(f),e=k+o*Math.sin(f),v,_,n,o,r,0,i,[f,T,g,k])}b=f-u;let M=Math.cos(u),m=Math.sin(u),P=Math.cos(f),x=Math.sin(f),w=Math.tan(b/4),L=4/3*n*w,A=4/3*o*w,V=[a,t],D=[a+L*m,t-A*M],C=[s+L*x,e-A*P],Mt=[s,e];if(D[0]=2*V[0]-D[0],D[1]=2*V[1]-D[1],l)return[D,C,Mt].concat(p);{p=[D,C,Mt].concat(p);let T=[];for(let v=0;v<p.length;v+=3){let _=R(p[v][0],p[v][1],c),W=R(p[v+1][0],p[v+1][1],c),E=R(p[v+2][0],p[v+2][1],c);T.push([_[0],_[1],W[0],W[1],E[0],E[1]])}return T}}var Gt={randOffset:function(a,t){return y(a,t)},randOffsetWithRange:function(a,t,s){return J(a,t,s)},ellipse:function(a,t,s,e,n){let o=At(s,e,n);return lt(a,t,n,o).opset},doubleLineOps:function(a,t,s,e,n){return I(a,t,s,e,n,!0)}};function Dt(a,t,s,e,n){return{type:"path",ops:I(a,t,s,e,n)}}function N(a,t,s){let e=(a||[]).length;if(e>2){let n=[];for(let o=0;o<e-1;o++)n.push(...I(a[o][0],a[o][1],a[o+1][0],a[o+1][1],s));return t&&n.push(...I(a[e-1][0],a[e-1][1],a[0][0],a[0][1],s)),{type:"path",ops:n}}return e===2?Dt(a[0][0],a[0][1],a[1][0],a[1][1],s):{type:"path",ops:[]}}function $t(a,t,s,e,n){return(function(o,r){return N(o,!0,r)})([[a,t],[a+s,t],[a+s,t+e],[a,t+e]],n)}function yt(a,t){if(a.length){let s=typeof a[0][0]=="number"?[a]:a,e=Q(s[0],1*(1+.2*t.roughness),t),n=t.disableMultiStroke?[]:Q(s[0],1.5*(1+.22*t.roughness),xt(t));for(let o=1;o<s.length;o++){let r=s[o];if(r.length){let h=Q(r,1*(1+.2*t.roughness),t),i=t.disableMultiStroke?[]:Q(r,1.5*(1+.22*t.roughness),xt(t));for(let l of h)l.op!=="move"&&e.push(l);for(let l of i)l.op!=="move"&&n.push(l)}}return{type:"path",ops:e.concat(n)}}return{type:"path",ops:[]}}function At(a,t,s){let e=Math.sqrt(2*Math.PI*Math.sqrt((Math.pow(a/2,2)+Math.pow(t/2,2))/2)),n=Math.ceil(Math.max(s.curveStepCount,s.curveStepCount/Math.sqrt(200)*e)),o=2*Math.PI/n,r=Math.abs(a/2),h=Math.abs(t/2),i=1-s.curveFitting;return r+=y(r*i,s),h+=y(h*i,s),{increment:o,rx:r,ry:h}}function lt(a,t,s,e){let[n,o]=Pt(e.increment,a,t,e.rx,e.ry,1,e.increment*J(.1,J(.4,1,s),s),s),r=K(n,null,s);if(!s.disableMultiStroke&&s.roughness!==0){let[h]=Pt(e.increment,a,t,e.rx,e.ry,1.5,0,s),i=K(h,null,s);r=r.concat(i)}return{estimatedPoints:o,opset:{type:"path",ops:r}}}function mt(a,t,s,e,n,o,r,h,i){let l=a,c=t,d=Math.abs(s/2),p=Math.abs(e/2);d+=y(.01*d,i),p+=y(.01*p,i);let u=n,f=o;for(;u<0;)u+=2*Math.PI,f+=2*Math.PI;f-u>2*Math.PI&&(u=0,f=2*Math.PI);let g=2*Math.PI/i.curveStepCount,k=Math.min(g/2,(f-u)/2),b=vt(k,l,c,d,p,u,f,1,i);if(!i.disableMultiStroke){let M=vt(k,l,c,d,p,u,f,1.5,i);b.push(...M)}return r&&(h?b.push(...I(l,c,l+d*Math.cos(u),c+p*Math.sin(u),i),...I(l,c,l+d*Math.cos(f),c+p*Math.sin(f),i)):b.push({op:"lineTo",data:[l,c]},{op:"lineTo",data:[l+d*Math.cos(u),c+p*Math.sin(u)]})),{type:"path",ops:b}}function wt(a,t){let s=Lt(Ot(gt(a))),e=[],n=[0,0],o=[0,0];for(let{key:r,data:h}of s)switch(r){case"M":o=[h[0],h[1]],n=[h[0],h[1]];break;case"L":e.push(...I(o[0],o[1],h[0],h[1],t)),o=[h[0],h[1]];break;case"C":{let[i,l,c,d,p,u]=h;e.push(...Rt(i,l,c,d,p,u,o,t)),o=[p,u];break}case"Z":e.push(...I(o[0],o[1],n[0],n[1],t)),o=[n[0],n[1]]}return{type:"path",ops:e}}function st(a,t){let s=[];for(let e of a)if(e.length){let n=t.maxRandomnessOffset||0,o=e.length;if(o>2){s.push({op:"move",data:[e[0][0]+y(n,t),e[0][1]+y(n,t)]});for(let r=1;r<o;r++)s.push({op:"lineTo",data:[e[r][0]+y(n,t),e[r][1]+y(n,t)]})}}return{type:"fillPath",ops:s}}function G(a,t){return(function(s,e){let n=s.fillStyle||"hachure";if(!S[n])switch(n){case"zigzag":S[n]||(S[n]=new at(e));break;case"cross-hatch":S[n]||(S[n]=new ot(e));break;case"dots":S[n]||(S[n]=new ht(e));break;case"dashed":S[n]||(S[n]=new rt(e));break;case"zigzag-line":S[n]||(S[n]=new it(e));break;default:n="hachure",S[n]||(S[n]=new q(e))}return S[n]})(t,Gt).fillPolygons(a,t)}function xt(a){let t=Object.assign({},a);return t.randomizer=void 0,a.seed&&(t.seed=a.seed+1),t}function _t(a){return a.randomizer||(a.randomizer=new ct(a.seed||0)),a.randomizer.next()}function J(a,t,s,e=1){return s.roughness*e*(_t(s)*(t-a)+a)}function y(a,t,s=1){return J(-a,a,t,s)}function I(a,t,s,e,n,o=!1){let r=o?n.disableMultiStrokeFill:n.disableMultiStroke,h=ut(a,t,s,e,n,!0,!1);if(r)return h;let i=ut(a,t,s,e,n,!0,!0);return h.concat(i)}function ut(a,t,s,e,n,o,r){let h=Math.pow(a-s,2)+Math.pow(t-e,2),i=Math.sqrt(h),l=1;l=i<200?1:i>500?.4:-.0016668*i+1.233334;let c=n.maxRandomnessOffset||0;c*c*100>h&&(c=i/10);let d=c/2,p=.2+.2*_t(n),u=n.bowing*n.maxRandomnessOffset*(e-t)/200,f=n.bowing*n.maxRandomnessOffset*(a-s)/200;u=y(u,n,l),f=y(f,n,l);let g=[],k=()=>y(d,n,l),b=()=>y(c,n,l),M=n.preserveVertices;return o&&(r?g.push({op:"move",data:[a+(M?0:k()),t+(M?0:k())]}):g.push({op:"move",data:[a+(M?0:y(c,n,l)),t+(M?0:y(c,n,l))]})),r?g.push({op:"bcurveTo",data:[u+a+(s-a)*p+k(),f+t+(e-t)*p+k(),u+a+2*(s-a)*p+k(),f+t+2*(e-t)*p+k(),s+(M?0:k()),e+(M?0:k())]}):g.push({op:"bcurveTo",data:[u+a+(s-a)*p+b(),f+t+(e-t)*p+b(),u+a+2*(s-a)*p+b(),f+t+2*(e-t)*p+b(),s+(M?0:b()),e+(M?0:b())]}),g}function Q(a,t,s){if(!a.length)return[];let e=[];e.push([a[0][0]+y(t,s),a[0][1]+y(t,s)]),e.push([a[0][0]+y(t,s),a[0][1]+y(t,s)]);for(let n=1;n<a.length;n++)e.push([a[n][0]+y(t,s),a[n][1]+y(t,s)]),n===a.length-1&&e.push([a[n][0]+y(t,s),a[n][1]+y(t,s)]);return K(e,null,s)}function K(a,t,s){let e=a.length,n=[];if(e>3){let o=[],r=1-s.curveTightness;n.push({op:"move",data:[a[1][0],a[1][1]]});for(let h=1;h+2<e;h++){let i=a[h];o[0]=[i[0],i[1]],o[1]=[i[0]+(r*a[h+1][0]-r*a[h-1][0])/6,i[1]+(r*a[h+1][1]-r*a[h-1][1])/6],o[2]=[a[h+1][0]+(r*a[h][0]-r*a[h+2][0])/6,a[h+1][1]+(r*a[h][1]-r*a[h+2][1])/6],o[3]=[a[h+1][0],a[h+1][1]],n.push({op:"bcurveTo",data:[o[1][0],o[1][1],o[2][0],o[2][1],o[3][0],o[3][1]]})}if(t&&t.length===2){let h=s.maxRandomnessOffset;n.push({op:"lineTo",data:[t[0]+y(h,s),t[1]+y(h,s)]})}}else e===3?(n.push({op:"move",data:[a[1][0],a[1][1]]}),n.push({op:"bcurveTo",data:[a[1][0],a[1][1],a[2][0],a[2][1],a[2][0],a[2][1]]})):e===2&&n.push(...ut(a[0][0],a[0][1],a[1][0],a[1][1],s,!0,!0));return n}function Pt(a,t,s,e,n,o,r,h){let i=[],l=[];if(h.roughness===0){a/=4,l.push([t+e*Math.cos(-a),s+n*Math.sin(-a)]);for(let c=0;c<=2*Math.PI;c+=a){let d=[t+e*Math.cos(c),s+n*Math.sin(c)];i.push(d),l.push(d)}l.push([t+e*Math.cos(0),s+n*Math.sin(0)]),l.push([t+e*Math.cos(a),s+n*Math.sin(a)])}else{let c=y(.5,h)-Math.PI/2;l.push([y(o,h)+t+.9*e*Math.cos(c-a),y(o,h)+s+.9*n*Math.sin(c-a)]);let d=2*Math.PI+c-.01;for(let p=c;p<d;p+=a){let u=[y(o,h)+t+e*Math.cos(p),y(o,h)+s+n*Math.sin(p)];i.push(u),l.push(u)}l.push([y(o,h)+t+e*Math.cos(c+2*Math.PI+.5*r),y(o,h)+s+n*Math.sin(c+2*Math.PI+.5*r)]),l.push([y(o,h)+t+.98*e*Math.cos(c+r),y(o,h)+s+.98*n*Math.sin(c+r)]),l.push([y(o,h)+t+.9*e*Math.cos(c+.5*r),y(o,h)+s+.9*n*Math.sin(c+.5*r)])}return[l,i]}function vt(a,t,s,e,n,o,r,h,i){let l=o+y(.1,i),c=[];c.push([y(h,i)+t+.9*e*Math.cos(l-a),y(h,i)+s+.9*n*Math.sin(l-a)]);for(let d=l;d<=r;d+=a)c.push([y(h,i)+t+e*Math.cos(d),y(h,i)+s+n*Math.sin(d)]);return c.push([t+e*Math.cos(r),s+n*Math.sin(r)]),c.push([t+e*Math.cos(r),s+n*Math.sin(r)]),K(c,null,i)}function Rt(a,t,s,e,n,o,r,h){let i=[],l=[h.maxRandomnessOffset||1,(h.maxRandomnessOffset||1)+.3],c=[0,0],d=h.disableMultiStroke?1:2,p=h.preserveVertices;for(let u=0;u<d;u++)u===0?i.push({op:"move",data:[r[0],r[1]]}):i.push({op:"move",data:[r[0]+(p?0:y(l[0],h)),r[1]+(p?0:y(l[0],h))]}),c=p?[n,o]:[n+y(l[u],h),o+y(l[u],h)],i.push({op:"bcurveTo",data:[a+y(l[u],h),t+y(l[u],h),s+y(l[u],h),e+y(l[u],h),c[0],c[1]]});return i}function j(a){return[...a]}function St(a,t=0){let s=a.length;if(s<3)throw new Error("A curve must have at least three points.");let e=[];if(s===3)e.push(j(a[0]),j(a[1]),j(a[2]),j(a[2]));else{let n=[];n.push(a[0],a[0]);for(let h=1;h<a.length;h++)n.push(a[h]),h===a.length-1&&n.push(a[h]);let o=[],r=1-t;e.push(j(n[0]));for(let h=1;h+2<n.length;h++){let i=n[h];o[0]=[i[0],i[1]],o[1]=[i[0]+(r*n[h+1][0]-r*n[h-1][0])/6,i[1]+(r*n[h+1][1]-r*n[h-1][1])/6],o[2]=[n[h+1][0]+(r*n[h][0]-r*n[h+2][0])/6,n[h+1][1]+(r*n[h][1]-r*n[h+2][1])/6],o[3]=[n[h+1][0],n[h+1][1]],e.push(o[1],o[2],o[3])}}return e}function B(a,t){return Math.pow(a[0]-t[0],2)+Math.pow(a[1]-t[1],2)}function jt(a,t,s){let e=B(t,s);if(e===0)return B(a,t);let n=((a[0]-t[0])*(s[0]-t[0])+(a[1]-t[1])*(s[1]-t[1]))/e;return n=Math.max(0,Math.min(1,n)),B(a,z(t,s,n))}function z(a,t,s){return[a[0]+(t[0]-a[0])*s,a[1]+(t[1]-a[1])*s]}function pt(a,t,s,e){let n=e||[];if((function(h,i){let l=h[i+0],c=h[i+1],d=h[i+2],p=h[i+3],u=3*c[0]-2*l[0]-p[0];u*=u;let f=3*c[1]-2*l[1]-p[1];f*=f;let g=3*d[0]-2*p[0]-l[0];g*=g;let k=3*d[1]-2*p[1]-l[1];return k*=k,u<g&&(u=g),f<k&&(f=k),u+f})(a,t)<s){let h=a[t+0];n.length?(o=n[n.length-1],r=h,Math.sqrt(B(o,r))>1&&n.push(h)):n.push(h),n.push(a[t+3])}else{let i=a[t+0],l=a[t+1],c=a[t+2],d=a[t+3],p=z(i,l,.5),u=z(l,c,.5),f=z(c,d,.5),g=z(p,u,.5),k=z(u,f,.5),b=z(g,k,.5);pt([i,p,g,b],0,s,n),pt([b,k,f,d],0,s,n)}var o,r;return n}function qt(a,t){return U(a,0,a.length,t)}function U(a,t,s,e,n){let o=n||[],r=a[t],h=a[s-1],i=0,l=1;for(let c=t+1;c<s-1;++c){let d=jt(a[c],r,h);d>i&&(i=d,l=c)}return Math.sqrt(i)>e?(U(a,t,l+1,e,o),U(a,l,s,e,o)):(o.length||o.push(r),o.push(h)),o}function nt(a,t=.15,s){let e=[],n=(a.length-1)/3;for(let o=0;o<n;o++)pt(a,3*o,t,e);return s&&s>0?U(e,0,e.length,s):e}var O="none",$=class{constructor(t){this.defaultOptions={maxRandomnessOffset:2,roughness:1,bowing:1,stroke:"#000",strokeWidth:1,curveTightness:0,curveFitting:.95,curveStepCount:9,fillStyle:"hachure",fillWeight:-1,hachureAngle:-41,hachureGap:-1,dashOffset:-1,dashGap:-1,zigzagOffset:-1,seed:0,disableMultiStroke:!1,disableMultiStrokeFill:!1,preserveVertices:!1,fillShapeRoughnessGain:.8},this.config=t||{},this.config.options&&(this.defaultOptions=this._o(this.config.options))}static newSeed(){return Math.floor(Math.random()*2**31)}_o(t){return t?Object.assign({},this.defaultOptions,t):this.defaultOptions}_d(t,s,e){return{shape:t,sets:s||[],options:e||this.defaultOptions}}line(t,s,e,n,o){let r=this._o(o);return this._d("line",[Dt(t,s,e,n,r)],r)}rectangle(t,s,e,n,o){let r=this._o(o),h=[],i=$t(t,s,e,n,r);if(r.fill){let l=[[t,s],[t+e,s],[t+e,s+n],[t,s+n]];r.fillStyle==="solid"?h.push(st([l],r)):h.push(G([l],r))}return r.stroke!==O&&h.push(i),this._d("rectangle",h,r)}ellipse(t,s,e,n,o){let r=this._o(o),h=[],i=At(e,n,r),l=lt(t,s,r,i);if(r.fill)if(r.fillStyle==="solid"){let c=lt(t,s,r,i).opset;c.type="fillPath",h.push(c)}else h.push(G([l.estimatedPoints],r));return r.stroke!==O&&h.push(l.opset),this._d("ellipse",h,r)}circle(t,s,e,n){let o=this.ellipse(t,s,e,e,n);return o.shape="circle",o}linearPath(t,s){let e=this._o(s);return this._d("linearPath",[N(t,!1,e)],e)}arc(t,s,e,n,o,r,h=!1,i){let l=this._o(i),c=[],d=mt(t,s,e,n,o,r,h,!0,l);if(h&&l.fill)if(l.fillStyle==="solid"){let p=Object.assign({},l);p.disableMultiStroke=!0;let u=mt(t,s,e,n,o,r,!0,!1,p);u.type="fillPath",c.push(u)}else c.push((function(p,u,f,g,k,b,M){let m=p,P=u,x=Math.abs(f/2),w=Math.abs(g/2);x+=y(.01*x,M),w+=y(.01*w,M);let L=k,A=b;for(;L<0;)L+=2*Math.PI,A+=2*Math.PI;A-L>2*Math.PI&&(L=0,A=2*Math.PI);let V=(A-L)/M.curveStepCount,D=[];for(let C=L;C<=A;C+=V)D.push([m+x*Math.cos(C),P+w*Math.sin(C)]);return D.push([m+x*Math.cos(A),P+w*Math.sin(A)]),D.push([m,P]),G([D],M)})(t,s,e,n,o,r,l));return l.stroke!==O&&c.push(d),this._d("arc",c,l)}curve(t,s){let e=this._o(s),n=[],o=yt(t,e);if(e.fill&&e.fill!==O)if(e.fillStyle==="solid"){let r=yt(t,Object.assign(Object.assign({},e),{disableMultiStroke:!0,roughness:e.roughness?e.roughness+e.fillShapeRoughnessGain:0}));n.push({type:"fillPath",ops:this._mergedShape(r.ops)})}else{let r=[],h=t;if(h.length){let i=typeof h[0][0]=="number"?[h]:h;for(let l of i)l.length<3?r.push(...l):l.length===3?r.push(...nt(St([l[0],l[0],l[1],l[2]]),10,(1+e.roughness)/2)):r.push(...nt(St(l),10,(1+e.roughness)/2))}r.length&&n.push(G([r],e))}return e.stroke!==O&&n.push(o),this._d("curve",n,e)}polygon(t,s){let e=this._o(s),n=[],o=N(t,!0,e);return e.fill&&(e.fillStyle==="solid"?n.push(st([t],e)):n.push(G([t],e))),e.stroke!==O&&n.push(o),this._d("polygon",n,e)}path(t,s){let e=this._o(s),n=[];if(!t)return this._d("path",n,e);t=(t||"").replace(/\n/g," ").replace(/(-\s)/g,"-").replace("/(ss)/g"," ");let o=e.fill&&e.fill!=="transparent"&&e.fill!==O,r=e.stroke!==O,h=!!(e.simplification&&e.simplification<1),i=(function(c,d,p){let u=Lt(Ot(gt(c))),f=[],g=[],k=[0,0],b=[],M=()=>{b.length>=4&&g.push(...nt(b,d)),b=[]},m=()=>{M(),g.length&&(f.push(g),g=[])};for(let{key:x,data:w}of u)switch(x){case"M":m(),k=[w[0],w[1]],g.push(k);break;case"L":M(),g.push([w[0],w[1]]);break;case"C":if(!b.length){let L=g.length?g[g.length-1]:k;b.push([L[0],L[1]])}b.push([w[0],w[1]]),b.push([w[2],w[3]]),b.push([w[4],w[5]]);break;case"Z":M(),g.push([k[0],k[1]])}if(m(),!p)return f;let P=[];for(let x of f){let w=qt(x,p);w.length&&P.push(w)}return P})(t,1,h?4-4*(e.simplification||1):(1+e.roughness)/2),l=wt(t,e);if(o)if(e.fillStyle==="solid")if(i.length===1){let c=wt(t,Object.assign(Object.assign({},e),{disableMultiStroke:!0,roughness:e.roughness?e.roughness+e.fillShapeRoughnessGain:0}));n.push({type:"fillPath",ops:this._mergedShape(c.ops)})}else n.push(st(i,e));else n.push(G(i,e));return r&&(h?i.forEach((c=>{n.push(N(c,!1,e))})):n.push(l)),this._d("path",n,e)}opsToPath(t,s){let e="";for(let n of t.ops){let o=typeof s=="number"&&s>=0?n.data.map((r=>+r.toFixed(s))):n.data;switch(n.op){case"move":e+=`M${o[0]} ${o[1]} `;break;case"bcurveTo":e+=`C${o[0]} ${o[1]}, ${o[2]} ${o[3]}, ${o[4]} ${o[5]} `;break;case"lineTo":e+=`L${o[0]} ${o[1]} `}}return e.trim()}toPaths(t){let s=t.sets||[],e=t.options||this.defaultOptions,n=[];for(let o of s){let r=null;switch(o.type){case"path":r={d:this.opsToPath(o),stroke:e.stroke,strokeWidth:e.strokeWidth,fill:O};break;case"fillPath":r={d:this.opsToPath(o),stroke:O,strokeWidth:0,fill:e.fill||O};break;case"fillSketch":r=this.fillSketch(o,e)}r&&n.push(r)}return n}fillSketch(t,s){let e=s.fillWeight;return e<0&&(e=s.strokeWidth/2),{d:this.opsToPath(t),stroke:s.fill||O,strokeWidth:e,fill:O}}_mergedShape(t){return t.filter(((s,e)=>e===0||s.op!=="move"))}},ft=class{constructor(t,s){this.canvas=t,this.ctx=this.canvas.getContext("2d"),this.gen=new $(s)}draw(t){let s=t.sets||[],e=t.options||this.getDefaultOptions(),n=this.ctx,o=t.options.fixedDecimalPlaceDigits;for(let r of s)switch(r.type){case"path":n.save(),n.strokeStyle=e.stroke==="none"?"transparent":e.stroke,n.lineWidth=e.strokeWidth,e.strokeLineDash&&n.setLineDash(e.strokeLineDash),e.strokeLineDashOffset&&(n.lineDashOffset=e.strokeLineDashOffset),this._drawToContext(n,r,o),n.restore();break;case"fillPath":{n.save(),n.fillStyle=e.fill||"";let h=t.shape==="curve"||t.shape==="polygon"||t.shape==="path"?"evenodd":"nonzero";this._drawToContext(n,r,o,h),n.restore();break}case"fillSketch":this.fillSketch(n,r,e)}}fillSketch(t,s,e){let n=e.fillWeight;n<0&&(n=e.strokeWidth/2),t.save(),e.fillLineDash&&t.setLineDash(e.fillLineDash),e.fillLineDashOffset&&(t.lineDashOffset=e.fillLineDashOffset),t.strokeStyle=e.fill||"",t.lineWidth=n,this._drawToContext(t,s,e.fixedDecimalPlaceDigits),t.restore()}_drawToContext(t,s,e,n="nonzero"){t.beginPath();for(let o of s.ops){let r=typeof e=="number"&&e>=0?o.data.map((h=>+h.toFixed(e))):o.data;switch(o.op){case"move":t.moveTo(r[0],r[1]);break;case"bcurveTo":t.bezierCurveTo(r[0],r[1],r[2],r[3],r[4],r[5]);break;case"lineTo":t.lineTo(r[0],r[1])}}s.type==="fillPath"?t.fill(n):t.stroke()}get generator(){return this.gen}getDefaultOptions(){return this.gen.defaultOptions}line(t,s,e,n,o){let r=this.gen.line(t,s,e,n,o);return this.draw(r),r}rectangle(t,s,e,n,o){let r=this.gen.rectangle(t,s,e,n,o);return this.draw(r),r}ellipse(t,s,e,n,o){let r=this.gen.ellipse(t,s,e,n,o);return this.draw(r),r}circle(t,s,e,n){let o=this.gen.circle(t,s,e,n);return this.draw(o),o}linearPath(t,s){let e=this.gen.linearPath(t,s);return this.draw(e),e}polygon(t,s){let e=this.gen.polygon(t,s);return this.draw(e),e}arc(t,s,e,n,o,r,h=!1,i){let l=this.gen.arc(t,s,e,n,o,r,h,i);return this.draw(l),l}curve(t,s){let e=this.gen.curve(t,s);return this.draw(e),e}path(t,s){let e=this.gen.path(t,s);return this.draw(e),e}},H="http://www.w3.org/2000/svg",dt=class{constructor(t,s){this.svg=t,this.gen=new $(s)}draw(t){let s=t.sets||[],e=t.options||this.getDefaultOptions(),n=this.svg.ownerDocument||window.document,o=n.createElementNS(H,"g"),r=t.options.fixedDecimalPlaceDigits;for(let h of s){let i=null;switch(h.type){case"path":i=n.createElementNS(H,"path"),i.setAttribute("d",this.opsToPath(h,r)),i.setAttribute("stroke",e.stroke),i.setAttribute("stroke-width",e.strokeWidth+""),i.setAttribute("fill","none"),e.strokeLineDash&&i.setAttribute("stroke-dasharray",e.strokeLineDash.join(" ").trim()),e.strokeLineDashOffset&&i.setAttribute("stroke-dashoffset",`${e.strokeLineDashOffset}`);break;case"fillPath":i=n.createElementNS(H,"path"),i.setAttribute("d",this.opsToPath(h,r)),i.setAttribute("stroke","none"),i.setAttribute("stroke-width","0"),i.setAttribute("fill",e.fill||""),t.shape!=="curve"&&t.shape!=="polygon"||i.setAttribute("fill-rule","evenodd");break;case"fillSketch":i=this.fillSketch(n,h,e)}i&&o.appendChild(i)}return o}fillSketch(t,s,e){let n=e.fillWeight;n<0&&(n=e.strokeWidth/2);let o=t.createElementNS(H,"path");return o.setAttribute("d",this.opsToPath(s,e.fixedDecimalPlaceDigits)),o.setAttribute("stroke",e.fill||""),o.setAttribute("stroke-width",n+""),o.setAttribute("fill","none"),e.fillLineDash&&o.setAttribute("stroke-dasharray",e.fillLineDash.join(" ").trim()),e.fillLineDashOffset&&o.setAttribute("stroke-dashoffset",`${e.fillLineDashOffset}`),o}get generator(){return this.gen}getDefaultOptions(){return this.gen.defaultOptions}opsToPath(t,s){return this.gen.opsToPath(t,s)}line(t,s,e,n,o){let r=this.gen.line(t,s,e,n,o);return this.draw(r)}rectangle(t,s,e,n,o){let r=this.gen.rectangle(t,s,e,n,o);return this.draw(r)}ellipse(t,s,e,n,o){let r=this.gen.ellipse(t,s,e,n,o);return this.draw(r)}circle(t,s,e,n){let o=this.gen.circle(t,s,e,n);return this.draw(o)}linearPath(t,s){let e=this.gen.linearPath(t,s);return this.draw(e)}polygon(t,s){let e=this.gen.polygon(t,s);return this.draw(e)}arc(t,s,e,n,o,r,h=!1,i){let l=this.gen.arc(t,s,e,n,o,r,h,i);return this.draw(l)}curve(t,s){let e=this.gen.curve(t,s);return this.draw(e)}path(t,s){let e=this.gen.path(t,s);return this.draw(e)}},Ft={canvas:(a,t)=>new ft(a,t),svg:(a,t)=>new dt(a,t),generator:a=>new $(a),newSeed:()=>$.newSeed()};
    return Ft;
    })();

    function render({ model, el }) {
      const W = model.get("width"), H = model.get("height");
      el.innerHTML = "";
      const svg = d3.select(el).append("svg")
        .attr("viewBox", `0 0 ${W} ${H}`)
        .style("max-width", "100%").style("height", "auto");

      const nodes = model.get("nodes").map(d => ({...d}));
      const links = model.get("links").map(d => ({...d}));
      const byId = new Map(nodes.map(d => [d.id, d]));
      links.forEach(l => { l.source = byId.get(l.source); l.target = byId.get(l.target); });
      const straight = links.filter(l => l.source !== l.target);
      const loops = links.filter(l => l.source === l.target);

      // Drawn, not plotted: rough.js puts every line and every disc on the page
      // the way a pen does — the stroke bows a little on the way across, and the
      // circle does not quite close where it started.
      //
      // Every shape carries a FIXED seed (its index + 1, because rough reads a
      // seed of 0 as "reseed from Math.random"), so a line keeps the same wobble
      // while the student drags its endpoints around. Reseeding per frame makes
      // the whole drawing vibrate, which is the one thing a hand-drawn look must
      // not do.
      //
      // The stroke is DOUBLE (rough's default), not a single pass. A single
      // pass at this roughness is a straight line at a glance — measured on
      // the module's own 12-dot ring, where the edges run ~145px and the
      // displacement rounds away to nothing. Two passes are what read as
      // drawn without the passes flying apart, which they start to do above
      // roughness ~1.6. Both passes come back inside ONE path, so the second
      // one costs no extra DOM.
      //
      // Past ~120 edges, regenerating the sketch on every frame costs more than
      // the look is worth, so a big graph falls back to straight strokes under
      // the older turbulence filter. Both paths render edges as <path>, so only
      // the `d` differs.
      const gen = rough.generator();
      const HAND = links.length <= 120;
      const PEN = { roughness: 1.4, bowing: 2 };
      const dOf = (drawable) => gen.toPaths(drawable).map(p => p.d).join(" ");

      const fxid = `lh-pen-${Math.random().toString(36).slice(2, 9)}`;
      const fx = svg.append("defs").append("filter").attr("id", fxid)
        .attr("x", "-15%").attr("y", "-15%").attr("width", "130%").attr("height", "130%");
      fx.append("feTurbulence").attr("type", "fractalNoise")
        .attr("baseFrequency", "0.02").attr("numOctaves", 2).attr("seed", 7).attr("result", "n");
      fx.append("feDisplacementMap").attr("in", "SourceGraphic").attr("in2", "n")
        .attr("scale", 2.4).attr("xChannelSelector", "R").attr("yChannelSelector", "G");
      const pen = HAND ? null : `url(#${fxid})`;

      straight.forEach((l, i) => { l.seed = i + 1; });
      loops.forEach((l, i) => { l.seed = straight.length + i + 1; });

      const link = svg.append("g").attr("filter", pen).selectAll("path").data(straight).join("path")
        .attr("fill", "none")
        .attr("stroke", d => d.color || "#6A6D75")
        .attr("stroke-width", d => d.width || 2)
        .attr("stroke-linecap", "round");
      const loop = svg.append("g").attr("filter", pen).selectAll("path").data(loops).join("path")
        .attr("fill", "none")
        .attr("stroke", d => d.color || "#6A6D75")
        .attr("stroke-width", d => d.width || 2)
        .attr("stroke-linecap", "round");

      const node = svg.append("g").selectAll("g").data(nodes).join("g")
        .style("cursor", "grab");
      // The disc is sketched ONCE, at the origin, and then carried around by the
      // group's transform. Regenerating it per tick would make it seethe in
      // place. rough hands back one path for the fill and one for the outline,
      // so a node is a small <g> holding both.
      node.each(function (d, i) {
        const r = d.r || 16;
        const disc = gen.circle(0, 0, 2 * r, {
          roughness: 0.9, bowing: 1, seed: i + 1,
          fill: d.color || "#3959A6", fillStyle: "solid",
          stroke: "#1D1E21", strokeWidth: 1.8,
        });
        d3.select(this).selectAll("path").data(gen.toPaths(disc)).join("path")
          .attr("d", p => p.d)
          .attr("fill", p => p.fill)
          .attr("stroke", p => p.stroke)
          .attr("stroke-width", p => p.strokeWidth)
          .attr("stroke-linejoin", "round").attr("stroke-linecap", "round");
      });
      // Label ink follows the fill. White was hardcoded, which is 1.25:1 on the
      // neutral #E4E6EA and 2.93:1 on amber — so on cp2's ripple three of four
      // labels were invisible, including the D the question is about, and on
      // cp5's ring the amber friends were the least legible nodes in the figure.
      const inkFor = (hex) => {
        const lum = (h) => {
          const m = /^#?([0-9a-f]{6})$/i.exec(h || "");
          if (!m) return null;
          const n = parseInt(m[1], 16);
          const lin = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
          return 0.2126 * lin((n >> 16) & 255) + 0.7152 * lin((n >> 8) & 255) + 0.0722 * lin(n & 255);
        };
        const bg = lum(hex);
        if (bg == null) return "#1D1E21";
        // Take whichever ink reads better, rather than thresholding on white:
        // amber is the mid-luminance fill where white fails (2.93:1) and so does
        // a mid-grey ink — #1D1E21 clears it at 5.68:1, and this also covers any
        // fill added later.
        const ratio = (a, b) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
        return ratio(bg, lum("#FFFFFF")) >= ratio(bg, lum("#1D1E21")) ? "#FFFFFF" : "#1D1E21";
      };
      node.append("text")
        .text(d => d.label ?? d.id)
        .attr("text-anchor", "middle").attr("dy", "0.35em")
        .attr("fill", d => inkFor(d.color || "#3959A6"))
        // A node label is the one thing in the figure that has to be READ, so it
        // is set in the page's own sans, not in a drawn face.
        .style("font", "600 13px system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', 'Liberation Sans', Arial, sans-serif")
        .style("pointer-events", "none");

      function place() {
        link.attr("d", d => HAND
          ? dOf(gen.line(d.source.x, d.source.y, d.target.x, d.target.y, {...PEN, seed: d.seed}))
          : `M ${d.source.x} ${d.source.y} L ${d.target.x} ${d.target.y}`);
        loop.attr("d", d => {
          const x = d.source.x, y = d.source.y, r = d.source.r || 16;
          const arc = `M ${x - 6} ${y - r + 4} C ${x - 30} ${y - r - 34}, ${x + 30} ${y - r - 34}, ${x + 6} ${y - r + 4}`;
          return HAND ? dOf(gen.path(arc, {...PEN, seed: d.seed})) : arc;
        });
        node.attr("transform", d => `translate(${d.x},${d.y})`);
      }

      const hasPos = nodes.every(d => d.x != null && d.y != null);
      if (hasPos && !model.get("physics")) {
        place();
        node.call(d3.drag().on("drag", (ev, d) => { d.x = ev.x; d.y = ev.y; place(); }));
      } else {
        const sim = d3.forceSimulation(nodes)
          .force("link", d3.forceLink(links).distance(70).strength(0.8))
          .force("charge", d3.forceManyBody().strength(-220))
          .force("center", d3.forceCenter(W / 2, H / 2))
          .force("collide", d3.forceCollide(24))
          .on("tick", place);
        node.call(d3.drag()
          .on("start", (ev, d) => { if (!ev.active) sim.alphaTarget(0.25).restart(); d.fx = d.x; d.fy = d.y; })
          .on("drag", (ev, d) => { d.fx = ev.x; d.fy = ev.y; })
          .on("end", (ev, d) => { if (!ev.active) sim.alphaTarget(0); d.fx = d.fy = null; }));
      }
    }
    export default { render };
    """
        nodes = _traitlets.List([]).tag(sync=True)
        links = _traitlets.List([]).tag(sync=True)
        width = _traitlets.Int(560).tag(sync=True)
        height = _traitlets.Int(420).tag(sync=True)
        physics = _traitlets.Bool(False).tag(sync=True)

    def netviz(
        edges,
        highlight=(),
        node_colors=None,
        nodes=None,
        layout="circle",
        physics=False,
        width=560,
        height=420,
    ):
        """Draw a small network as a themed, drag-able D3 widget.

        edges: [(u, v), ...] — node names appear in first-seen order;
               (u, u) draws a self-loop arc above the node.
        highlight: edges to paint rust-red (e.g. shortcuts).
        node_colors: {node: "#hex"} overrides (default themed blue).
        nodes: extra nodes to include even if they have no edges.
        layout: "circle" (default), a {node: (x, y)} dict with 0..1 coords,
                or None for a live force layout. physics=True also forces it.
        """
        import math

        ids = []
        for _u, _v in edges:
            for _t in (_u, _v):
                if _t not in ids:
                    ids.append(_t)
        for _t in nodes or []:
            if _t not in ids:
                ids.append(_t)
        node_colors = node_colors or {}
        hi = {frozenset(e) for e in highlight}
        pos = {}
        if isinstance(layout, dict):
            pos = {k: (float(x), float(y)) for k, (x, y) in layout.items()}
        elif layout == "circle" and ids:
            for _i, _nid in enumerate(ids):
                _a = 2 * math.pi * _i / len(ids) - math.pi / 2
                pos[_nid] = (0.5 + 0.42 * math.cos(_a), 0.5 + 0.42 * math.sin(_a))
        # One scale for both axes, then centre: scaling 0..1 coords by width
        # and height separately turned every ring into a 4:3 ellipse.
        _s = min(width, height)
        _ox, _oy = (width - _s) / 2, (height - _s) / 2
        node_list = []
        for _nid in ids:
            _d = {"id": str(_nid), "color": node_colors.get(_nid, "#3959A6")}
            if _nid in pos:
                _d["x"] = _ox + pos[_nid][0] * _s
                _d["y"] = _oy + pos[_nid][1] * _s
            node_list.append(_d)
        link_list = [
            {
                "source": str(_u),
                "target": str(_v),
                **(
                    {"color": "#B14434", "width": 3.5}
                    if frozenset((_u, _v)) in hi
                    else {}
                ),
            }
            for _u, _v in edges
        ]
        return _NetViz(
            nodes=node_list,
            links=link_list,
            width=width,
            height=height,
            physics=bool(physics) or not pos,
        )

    return (netviz,)


@app.cell(hide_code=True)
def _(alt, ig, mo, netviz, np, nx, pd, plt):
    def run_student_code(code, env=None):
        """Run code from a fill-in exercise box; show stdout + last expression.

        Errors come back as one friendly line, not a wall of traceback."""
        import ast
        import contextlib
        import io

        ns = {
            "mo": mo, "ig": ig, "nx": nx, "np": np,
            "plt": plt, "alt": alt, "pd": pd, "netviz": netviz,
        }
        ns.update(env or {})
        buf = io.StringIO()
        try:
            tree = ast.parse(code or "", mode="exec")
            last = None
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last = ast.Expression(tree.body[-1].value)
                tree.body = tree.body[:-1]
            with contextlib.redirect_stdout(buf):
                exec(compile(tree, "<your code>", "exec"), ns)
                result = (
                    eval(compile(last, "<your code>", "eval"), ns)
                    if last is not None
                    else None
                )
        except Exception as e:
            line = getattr(e, "lineno", None)
            tb = getattr(e, "__traceback__", None)
            while tb is not None:
                if tb.tb_frame.f_code.co_filename == "<your code>":
                    line = tb.tb_lineno
                tb = tb.tb_next
            where = f" on line {line}" if line else ""
            return mo.md(
                f"🤔 **Python hiccup{where}:** `{type(e).__name__}: {e}`\n\n"
                "*Read it slowly — it usually names the problem. "
                "Fix it and press ▶ Run again.*"
            )
        parts = []
        if buf.getvalue():
            parts.append(mo.md(f"```\n{buf.getvalue()}\n```"))
        if result is not None:
            parts.append(result)
        if not parts:
            parts.append(
                mo.md(
                    "✅ *Ran without errors — nothing to display yet. "
                    "End with a bare value (like `my_L`) to show it.*"
                )
            )
        return mo.vstack(parts)

    return (run_student_code,)


@app.cell(hide_code=True)
def ch1_header(mo):
    mo.md(r"""
    ## Chapter 1 of 5 — A Letter Across a Country

    It begins with an experiment. In the 1960s, letters were mailed to strangers in Nebraska. Each one carried a single rule: pass it only to someone you know by first name. Each one had a single target, a stockbroker in Boston. How many hands does a letter like that need? My guess is below, next to what actually happened.
    """)
    return


@app.cell(hide_code=True)
def cp1_milgram_img(mo):
    mo.vstack([
        mo.image(
            src="assets/milgram-small-world-experiment.png",
            width=520,
            caption="Milgram's letter experiment (1960s)",
        ),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>Read the picture as a "
            "relay. A packet starts with a randomly chosen person in Omaha, "
            "Nebraska, and has to reach one named stockbroker near Boston. Nobody "
            "may post it directly: each holder passes it to a single person they "
            "know on a first-name basis and who they think sits closer to the "
            "target. Each arrow is one such hand-off. The drawing shows the idea, "
            "not the result.</span>"
        ),
    ])
    return


@app.cell(hide_code=True)
def cp1_milgram_note(mo):
    mo.md(r"""
    ### 🌍 Six degrees of separation
    In the 1960s, Stanley Milgram mailed packets to strangers in Nebraska
    with one rule: pass it to someone you know on a first-name basis,
    until it reaches a Boston stockbroker. The letters that arrived took
    about **6 hops** — 64 of the 296 packets made it, through **5.2
    intermediaries** on average. It has been re-measured twice since: a
    2003 email version (24,000 chains aimed at 18 targets in 13 countries)
    averaged about **4 steps** among the chains that finished, and a 2012
    study of Facebook's 721 million users found **4.74 steps**.
    """)
    return


@app.cell(hide_code=True)
def cp1_wikirace(mo):
    mo.vstack([
        mo.md("**Try it: Wikirace**"),
        mo.md(
            "<a href='https://wiki-race.com' target='_blank' rel='noopener' "
            "style='display:inline-block; padding:8px 18px; border:1px solid "
            "#3959A6; border-radius:10px; color:#3959A6; text-decoration:none; "
            "font-weight:600;'>▶ wiki-race.com</a>"
        ),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>Opens in a new tab, so "
            "this page stays where it is. The game hands you a **start** article "
            "and a **target** article. You have to reach the target by clicking. "
            "You may only use the links printed on the page you are standing on. "
            "No search box, no typing an address. Play a round if you feel like "
            "it, and keep count of your clicks.</span>"
        ),
    ])
    return


@app.cell(hide_code=True)
def cp1_routing_fig(mo, netviz):
    _edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
        (0, 2), (3, 5), (7, 9),
    ]
    _colors = {0: "#B14434", 1: "#DAB167", 2: "#DAB167", 11: "#DAB167", 6: "#3959A6"}
    mo.vstack([
        mo.md("**The letter-holder's view**"),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>The **rust** dot is "
            "whoever holds the letter right now. The **rust lines** are the only "
            "friendships they can see: the ones running to their own **amber** "
            "friends. The **navy** dot on the far side is the Boston target. "
            "Every **grey** dot and line exists, but the holder has no idea who "
            "out there knows whom. They pick ONE amber friend and hope. Dots are "
            "drag-able.</span>"
        ),
        netviz(
            _edges,
            highlight=[(0, 1), (0, 2), (0, 11)],
            node_colors={_n: _colors.get(_n, "#E4E6EA") for _n in range(12)},
        ),
    ])
    return


@app.cell(hide_code=True)
def cp1_routing_note(mo):
    mo.md(r"""
    ### 🧭 Existing vs. findable
    A short path **existing** somewhere in a network is a fact about the
    whole network — you'd need the full map to even check it. A short
    path being **found**, by ordinary people each using only who THEY
    personally knew, is a much stronger claim. Milgram's letter-holders
    never saw the social network as a whole; they just kept forwarding to
    whoever seemed "closer" to the target. That they succeeded, in about
    6 hops, is the surprising part.
    """)
    return


@app.cell(hide_code=True)
def ch2_header(mo):
    mo.md(r"""
    ## Chapter 2 of 5 — Measuring Smallness

    "Small" needs a number before it means anything. This chapter builds the module's measuring sticks. The first is distance: how many steps separate two people. We find it on a four-person network, and the same chart hides a second number, the worst-case trip. Then distance again, by hand, on paper. After that comes a family of measures distance cannot see at all. They are about the shape of one person's circle of friends. One person's own corner first. Then everyone's corners averaged. Then the whole network counted a third way, which does not agree with the second.
    """)
    return


@app.cell(hide_code=True)
def cp2_steps(mo):
    cp2_steps = mo.ui.slider(0, 3, value=0, step=1, label="steps from A")
    cp2_steps
    return (cp2_steps,)


@app.cell(hide_code=True)
def cp2_ripple_fig(cp2_steps, mo, netviz, nx):
    _edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D")]
    _G = nx.Graph()
    _G.add_edges_from(_edges)

    _reached = set()
    _frontier = {"A"}
    for _ in range(cp2_steps.value):
        _nxt = set()
        for _u in _frontier:
            for _v in _G[_u]:
                if _v != "A" and _v not in _reached:
                    _reached.add(_v)
                    _nxt.add(_v)
        _frontier = _nxt

    _colors = {
        _n: ("#B14434" if _n == "A" else ("#DAB167" if _n in _reached else "#E4E6EA"))
        for _n in _G.nodes()
    }
    mo.vstack([
        mo.md(
            f"**Wave from A — {cp2_steps.value} step(s)**\n\n"
            "<span style='color:#6A6D75;font-size:13px'>Four people, five "
            "friendships. **A** is rust. **Amber** dots are everyone A can reach "
            "in that many steps or fewer. **Grey** dots are still out of range. "
            "Drag the slider up one notch at a time and watch who joins. The "
            "step at which someone first turns amber IS their distance from A. "
            "You can drag the dots too; moving them changes nothing but the "
            "picture.</span>"
        ),
        netviz(_edges, node_colors=_colors),
    ])
    return


@app.cell(hide_code=True)
def cp2_pairs_fig(alt, mo, pd):
    _pairs = [("A", "B", 1), ("A", "C", 1), ("A", "D", 2), ("B", "C", 1), ("B", "D", 1), ("C", "D", 1)]
    _df = pd.DataFrame(_pairs, columns=["u", "v", "distance"])
    _df["pair"] = _df["u"] + "–" + _df["v"]
    _df["highlight"] = _df["distance"] > 1

    _base = alt.Chart(_df).encode(
        y=alt.Y("pair:N", sort=_df["pair"].tolist(), title=None),
    )
    _dots = _base.mark_point(filled=True, size=170, opacity=1).encode(
        x=alt.X(
            "distance:Q",
            title="shortest-path distance",
            scale=alt.Scale(domain=[0.6, 2.4]),
            axis=alt.Axis(values=[1, 2], grid=True),
        ),
        color=alt.condition("datum.highlight", alt.value("#B14434"), alt.value("#3959A6")),
        tooltip=["pair", "distance"],
    )
    _mean = alt.Chart(pd.DataFrame({"m": [_df["distance"].mean()]})).mark_rule(
        strokeDash=[4, 4], color="#6A6D75", opacity=0.8,
    ).encode(x="m:Q")
    _fig = (_mean + _dots).properties(
        title="All 6 pairs, distance — average 7/6 ≈ 1.17",
        height=220,
    )
    mo.vstack([
        _fig,
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>One dot per pair of "
            "people. With four people there are exactly six pairs, and every "
            "pair gets counted once. A dot's position along the axis is that "
            "pair's distance. A dot at 1 means they are directly connected. The "
            "**rust dot is the only pair that needs a detour**. The dashed grey "
            "line is the average of the six, which is the number in the "
            "title.</span>"
        ),
    ])
    return


@app.cell(hide_code=True)
def cp2_distance_note(mo):
    mo.md(r"""
    ### 📏 Distance and average path length
    The **distance** $d(u,v)$ between two people is the number of edges on
    the shortest route between them. Averaging over every pair gives the
    **average path length** $L$ — one number for how far apart a whole
    network sits:

    $$
    L = \frac{\text{every pair's } d(u,v)\text{, added up}}{\text{how many pairs there are}}
      = \frac{1 + 1 + 2 + 1 + 1 + 1}{6} = \frac{7}{6} \approx 1.17
    $$

    Five pairs sit at distance 1 here and A–D at 2. "Six degrees" is
    exactly this number, measured on a whole country.
    """)
    return


@app.cell(hide_code=True)
def cp2_diameter_note(mo):
    mo.md(r"""
    ### 📐 Diameter — the worst-case trip
    **Average path length** ($L$) is the typical trip; the **diameter**
    is the single LONGEST shortest-path trip anywhere in the network —
    the worst case, not the average. Here every pair sits at distance 1
    except A–D, so the diameter is **2**. A ring or lattice can have a
    diameter that keeps growing as the network grows; a small-world
    network's diameter stays small even as it gets bigger — that's part
    of what "small" means.
    """)
    return


@app.cell(hide_code=True)
def cp2_paperwork_photo(mo):
    from pathlib import Path as _P

    cp2_paperwork_photo = mo.ui.file(
        kind="area",
        filetypes=[".jpg", ".jpeg", ".png", ".webp"],
        label="Photo of your paper work",
    )
    # Once a photo has been saved, this cell is a caption rather than an
    # instruction. The drop area stays — replacing a photo is the intended
    # loop, and the notebook is live again whenever it is reopened — but a
    # finished keepsake should not still be asking its reader to go and take
    # a photograph. (The two cells below already hide themselves when done;
    # this one asked forever.) marimo forbids reading a UIElement's .value in
    # the cell that creates it, so the test is the saved file, not the widget.
    if _P("assets/uploads/cp2_paperwork_photo_view.jpg").exists():
        _caption = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*The photo of "
            "your paper working is below — drop another here only if you want to "
            "replace it.*</span>"
        )
    else:
        _caption = mo.md(
                "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
                "your paper here. Show the 5-dot ring, all 10 pairs with a "
                "distance beside each, and the average at the bottom. Working "
                "shown beats a tidy answer.</span>"
        )
    mo.vstack([cp2_paperwork_photo, _caption])
    return (cp2_paperwork_photo,)


@app.cell(hide_code=True)
def cp2_paperwork_photo_preview(cp2_paperwork_photo, mo):
    from pathlib import Path as _P

    _files = list(cp2_paperwork_photo.value or [])
    # A photo already saved means this session is over and someone is reading
    # the notebook. The drop box cannot remember the file across a restart, but
    # the saved copy is two cells below — so "your photo appears here once you
    # drop it in" was simply false to every later reader.
    _done = not _files and _P("assets/uploads/cp2_paperwork_photo_view.jpg").exists()
    cp2_paperwork_photo_send = mo.ui.run_button(label="📨 Send to my tutor", disabled=not _files)
    if _done:
        _out = None
    elif not _files:
        _out = mo.vstack([
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Your photo appears "
                "here once you drop it in above.*</span>"
            ),
            cp2_paperwork_photo_send,
        ])
    else:
        _out = mo.vstack([
            mo.image(_files[0].contents, width=420),
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>This is exactly what "
                "your tutor will see. Missed a pair, or want to redo the table? Drop "
                "another photo into the box above — it replaces this one, as many "
                "times as you like. When it looks right, press send.</span>"
            ),
            cp2_paperwork_photo_send,
        ])
    _out
    return (cp2_paperwork_photo_send,)


@app.cell(hide_code=True)
def cp2_paperwork_photo_sent(
    cp2_paperwork_photo,
    cp2_paperwork_photo_send,
    mo,
):
    from pathlib import Path as _P

    # Recomputed, not borrowed: a name starting with "_" is private to its cell
    # in marimo, so the preview cell's copy is not visible here.
    _done = not (cp2_paperwork_photo.value or []) and _P("assets/uploads/cp2_paperwork_photo_view.jpg").exists()
    if cp2_paperwork_photo_send.value and (cp2_paperwork_photo.value or []):

        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp2_paperwork_photo\n")
        _sent = mo.md("✅ **Sent.** Your tutor is looking at it now.")
    else:
        _sent = (
            None
            if _done
            else mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Press the button above "
                "when the photo looks right — that is what tells your tutor to look.*</span>"
            )
        )
    _sent
    return


@app.cell(hide_code=True)
def cp2_paperwork_note(mo):
    mo.md(r"""
    ### ✏️ By hand: distance on a 5-ring
    Same two ideas as before — $d(u,v)$, the distance between two people
    (the fewest lines you cross to get from $u$ to $v$), and $L$, the
    average of $d(u,v)$ over every pair — computed entirely on paper this
    time, on a network no widget ever showed. 5 pairs sit at distance 1
    and 5 "across the circle" pairs sit at distance 2:

    $$
    L = \frac{5 \times 1 + 5 \times 2}{10} = \frac{15}{10} = 1.5
    $$
    """)
    return


@app.cell(hide_code=True)
def cp3_fig(mo, netviz):
    _edges = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"), ("B", "F"), ("C", "E")]
    _friend_edges = [("B", "F"), ("C", "E")]
    mo.vstack([
        mo.md(
            "**A and A's five friends**\n\n"
            "<span style='color:#6A6D75;font-size:13px'>**A** is the rust dot in "
            "the middle; B, C, D, E and F are its five friends. The grey lines "
            "from A are A's own friendships — ignore those. The **rust lines run "
            "between two of A's friends**: those are the ones that say "
            "\"my friends know each other\". Find them and count them yourself. "
            "Dots are drag-able if the picture gets tangled.</span>"
        ),
        # A really IS in the middle — the caption and the describe line both say
        # so, and the default circle layout put it on the ring at the top, where
        # a reader hunting for a central rust dot found a hexagon.
        netviz(
            _edges,
            highlight=_friend_edges,
            node_colors={"A": "#B14434"},
            layout={"A": (0.5, 0.5), "B": (0.5, 0.14), "C": (0.842, 0.389), "D": (0.712, 0.791), "E": (0.288, 0.791), "F": (0.158, 0.389)},
        ),
    ])
    return


@app.cell(hide_code=True)
def cp3_clustering_note(mo):
    mo.md(r"""
    ### 🤝 Local clustering — do my friends know each other?
    The **local clustering coefficient** of a person $i$ counts the
    friendships among $i$'s own friends, against how many there could be:

    $$
    C_i = \frac{\text{friendships among } i\text{'s friends}}{\text{pairs of friends } i \text{ has}}
    \qquad\Longrightarrow\qquad
    C_A = \frac{2}{10} = 0.2
    $$

    A has 5 friends, so up to 10 friendships could exist among them; 2 do.
    That is one person's score; everybody in the picture has one of their
    own, and social networks typically run high.
    """)
    return


@app.cell(hide_code=True)
def cp3_average_note(mo):
    mo.md(r"""
    ### 👥 Average local clustering — one vote each
    Everyone has their own $C_i$ — the fraction of their friend-pairs who
    are friends. The **average local clustering** $\overline{C}$ is the
    plain mean of those over everybody. A scores $0.2$; B, C, E and F each
    know exactly two people who know each other, so each scores a perfect
    $1$; D, with a single friend, has no pair to check at all — by
    convention anyone with fewer than two friends scores $0$. So

    $$
    \overline{C} = \frac{\text{everyone's } C_i\text{, added up}}{\text{how many people there are}}
      = \frac{0.2 + 1 + 1 + 0 + 1 + 1}{6} = \frac{4.2}{6} = 0.70
    $$

    Everyone gets one equal vote, which is how four small, perfectly
    closed circles outvote the one hub whose own circle is nearly empty.
    """)
    return


@app.cell(hide_code=True)
def cp3_triplets_fig(mo, netviz):
    _edges = [("P", "Q"), ("Q", "R"), ("R", "P"), ("X", "Y"), ("X", "Z")]
    mo.vstack([
        mo.md("**Closed triplet (left) — open triplet (right)**"),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>Two trios. Left: P, Q "
            "and R, with **all three friendships there (rust)**. That is a "
            "**closed** triplet, better known as a triangle. Right: X knows Y "
            "and Z, but Y and Z never met. Still a triplet, just **open**: one "
            "line short of a triangle. A triplet is named by its middle person, "
            "which on the right is X. In a triangle every corner takes a turn "
            "in the middle. That is why one triangle shows up three times in a "
            "triplet count. Dots are drag-able.</span>"
        ),
        netviz(
            _edges,
            highlight=[("P", "Q"), ("Q", "R"), ("R", "P")],
            layout={
                "P": (0.25, 0.15), "Q": (0.08, 0.80), "R": (0.42, 0.80),
                "X": (0.75, 0.15), "Y": (0.58, 0.80), "Z": (0.92, 0.80),
            },
        ),
    ])
    return


@app.cell(hide_code=True)
def cp3_global_clustering_note(mo):
    mo.md(r"""
    ### 🔺 Global clustering — one number for the whole network
    A **triplet** is three people joined by at least two friendships,
    counted by the person in the middle — open and closed alike. A
    **triangle** is a triplet whose third friendship also exists. Someone
    with $k$ friends ($k$ = how many friends that person has) centers
    $k(k-1)/2$ triplets: Alice ($k=5$) centers 10, her other four friends
    center 1 each, D none — 14 in all, holding 2 triangles. The **global
    clustering coefficient** is

    $$
    C = \frac{3 \times \text{triangles}}{\text{triplets}}
      = \frac{3 \times 2}{14} = \frac{6}{14} \approx 0.43
    $$

    — the 3 because each triangle is counted once per corner. People who
    center more triplets get more say, so this number listens to hubs.

    **Same network, two answers:**

    $$
    \overline{C} = 0.70 \qquad\text{versus}\qquad C = 0.43
    $$

    Both are correct. The average counts PEOPLE, and four of the six here
    have tiny, perfectly closed circles that each score 1. The global one
    counts TRIPLETS, and Alice alone owns 10 of the 14 — only 2 of them
    closed. Reporting either as "the clustering coefficient" without
    saying which is how two papers end up impossible to compare.
    """)
    return


@app.cell(hide_code=True)
def ch3_header(mo):
    mo.md(r"""
    ## Chapter 3 of 5 — One Extra Line

    A ring of dots, and one extra cable to spend anywhere. Where should it go? That one choice opens this chapter's real question: what a single link can do to a whole network. From there we work out two formulas: how a ring's clustering behaves as the ring grows, and how its distances do.
    """)
    return


@app.cell(hide_code=True)
def cp4_photo(mo):
    from pathlib import Path as _P

    cp4_photo = mo.ui.file(
        kind="area",
        filetypes=[".jpg", ".jpeg", ".png", ".webp"],
        label="Photo of your drawing",
    )
    # Once a photo has been saved, this cell is a caption rather than an
    # instruction. The drop area stays — replacing a photo is the intended
    # loop, and the notebook is live again whenever it is reopened — but a
    # finished keepsake should not still be asking its reader to go and take
    # a photograph. (The two cells below already hide themselves when done;
    # this one asked forever.) marimo forbids reading a UIElement's .value in
    # the cell that creates it, so the test is the saved file, not the widget.
    if _P("assets/uploads/cp4_photo_view.jpg").exists():
        _caption = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*The photo of "
            "your ring drawing is below — drop another here only if you want to "
            "replace it.*</span>"
        )
    else:
        _caption = mo.md(
                "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
                "your 8-dot ring here — the drawing with your one extra cable on it. "
                "It does not need to be neat; it needs to show which two dots you "
                "joined.</span>"
        )
    mo.vstack([cp4_photo, _caption])
    return (cp4_photo,)


@app.cell(hide_code=True)
def cp4_photo_preview(cp4_photo, mo):
    from pathlib import Path as _P

    _files = list(cp4_photo.value or [])
    # A photo already saved means this session is over and someone is reading
    # the notebook. The drop box cannot remember the file across a restart, but
    # the saved copy is two cells below — so "your photo appears here once you
    # drop it in" was simply false to every later reader.
    _done = not _files and _P("assets/uploads/cp4_photo_view.jpg").exists()
    cp4_photo_send = mo.ui.run_button(label="📨 Send to my tutor", disabled=not _files)
    if _done:
        _out = None
    elif not _files:
        _out = mo.vstack([
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Your photo appears "
                "here once you drop it in above.*</span>"
            ),
            cp4_photo_send,
        ])
    else:
        _out = mo.vstack([
            mo.image(_files[0].contents, width=420),
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>This is exactly what "
                "your tutor will see. Not the one you meant? Drop another photo "
                "into the box above — it replaces this one, as many times as you "
                "like. When it looks right, press send.</span>"
            ),
            cp4_photo_send,
        ])
    _out
    return (cp4_photo_send,)


@app.cell(hide_code=True)
def cp4_photo_sent(cp4_photo, cp4_photo_send, mo):
    from pathlib import Path as _P

    # Recomputed, not borrowed: a name starting with "_" is private to its cell
    # in marimo, so the preview cell's copy is not visible here.
    _done = not (cp4_photo.value or []) and _P("assets/uploads/cp4_photo_view.jpg").exists()
    if cp4_photo_send.value and (cp4_photo.value or []):

        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp4_photo\n")
        _sent = mo.md("✅ **Sent.** Your tutor is looking at it now.")
    else:
        _sent = (
            None
            if _done
            else mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Press the button above "
                "when the photo looks right — that is what tells your tutor to look.*</span>"
            )
        )
    _sent
    return


@app.cell(hide_code=True)
def cp4_choice(mo):
    cp4_choice = mo.ui.radio(
        options=["no extra cable", "short cable (2 apart)", "long cable (opposite)"],
        value="no extra cable",
        label="Compare three placements",
    )
    cp4_choice
    return (cp4_choice,)


@app.cell(hide_code=True)
def cp4_compare_fig(cp4_choice, mo, netviz, nx):
    _edges = [(i, (i + 1) % 8) for i in range(8)]
    _extra = None
    if cp4_choice.value == "short cable (2 apart)":
        _extra = (0, 2)
    elif cp4_choice.value == "long cable (opposite)":
        _extra = (0, 4)
    _G = nx.cycle_graph(8)
    if _extra:
        _G.add_edge(*_extra)
        _edges.append(_extra)
    _L = nx.average_shortest_path_length(_G)

    mo.vstack([
        mo.md(
            f"**Average distance: {_L:.2f}**\n\n"
            "<span style='color:#6A6D75;font-size:13px'>The same 8-dot ring three "
            "times over. The **rust line is the one extra cable**; the number "
            "above is the average trip length over all 28 pairs, recomputed every "
            "time you switch. Flip between the three options and watch only that "
            "number: same ring, same single extra line, and the only thing that "
            "changed is where it was put.</span>"
        ),
        netviz(_edges, highlight=[_extra] if _extra else [], layout="circle"),
    ])
    return


@app.cell(hide_code=True)
def cp4_shortcut_drawing_note(mo):
    mo.md(r"""
    ### 🔌 One cable, two very different effects
    Same single line, two jobs. Between nearby dots it closes a
    **triangle** — clustering goes up. Across the ring it is a
    **shortcut** — trips get shorter for everyone at once. On this
    8-dot ring the average distance goes $2.29 \rightarrow 2.07$ with a
    short cable and $2.29 \rightarrow 1.96$ with a long one: about half
    again as much travel saved, from one line placed differently. WHERE
    a link goes matters more than HOW MANY links there are — and the
    bigger the ring, the wider that gap gets.
    """)
    return


@app.cell(hide_code=True)
def cp5_ring_controls(mo):
    cp5_ring_k = mo.ui.slider(
        steps=[2, 4, 6], value=2, label="k (friends per person)", show_value=True
    )
    cp5_ring_show = mo.ui.checkbox(
        value=False, label="check my count (highlight friendships among the amber dots)"
    )
    mo.hstack([cp5_ring_k, cp5_ring_show], justify="start", gap=2)
    return cp5_ring_k, cp5_ring_show


@app.cell(hide_code=True)
def cp5_ring_fig(cp5_ring_k, cp5_ring_show, mo, netviz):
    import math as _math

    _N = 12
    _k = cp5_ring_k.value
    _half = _k // 2

    # Explicit node order (0..N-1) for the circle layout — netviz's own
    # "circle" string layout orders nodes by first appearance in the edge
    # list, which a deduped/sorted edge set scrambles (a node can land in the
    # wrong slot). Position every node ourselves instead.
    _pos = {
        _i: (
            0.5 + 0.42 * _math.cos(2 * _math.pi * _i / _N - _math.pi / 2),
            0.5 + 0.42 * _math.sin(2 * _math.pi * _i / _N - _math.pi / 2),
        )
        for _i in range(_N)
    }
    _edges = [(_i, (_i + _d) % _N) for _i in range(_N) for _d in range(1, _half + 1)]
    _edge_lookup = {tuple(sorted(e)) for e in _edges}

    _friends = sorted({_d % _N for _d in range(1, _half + 1)} | {(-_d) % _N for _d in range(1, _half + 1)})
    _friend_pairs = [
        (_friends[_i], _friends[_j])
        for _i in range(len(_friends))
        for _j in range(_i + 1, len(_friends))
        if tuple(sorted((_friends[_i], _friends[_j]))) in _edge_lookup
    ]
    _node_colors = {0: "#B14434", **{_f: "#DAB167" for _f in _friends}}
    _hl = _friend_pairs if cp5_ring_show.value else []
    mo.vstack([
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>**Node 0** is the rust dot; "
            f"the **amber dots are its friends** ({_half} on each side). Every line "
            "is a friendship — the ones to count are the lines that join *two amber "
            "dots*. The slider changes how many friends each person has. The "
            "check-box paints those amber-to-amber lines rust once you have "
            "committed to a number, so you can check your own count.</span>"
        ),
        netviz(_edges, highlight=_hl, node_colors=_node_colors, layout=_pos),
    ])
    return


@app.cell(hide_code=True)
def cp5_ring_paperwork_photo(mo):
    from pathlib import Path as _P

    cp5_ring_paperwork_photo = mo.ui.file(
        kind="area",
        filetypes=[".jpg", ".jpeg", ".png", ".webp"],
        label="Photo of your ring working (triangles + formulas)",
    )
    # Once a photo has been saved, this cell is a caption rather than an
    # instruction. The drop area stays — replacing a photo is the intended
    # loop, and the notebook is live again whenever it is reopened — but a
    # finished keepsake should not still be asking its reader to go and take
    # a photograph. (The two cells below already hide themselves when done;
    # this one asked forever.) marimo forbids reading a UIElement's .value in
    # the cell that creates it, so the test is the saved file, not the widget.
    if _P("assets/uploads/cp5_ring_paperwork_photo_view.jpg").exists():
        _caption = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*The photo of "
            "your derivation is below — drop another here only if you want to "
            "replace it.*</span>"
        )
    else:
        _caption = mo.md(
                "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
                "your derivation here. Show node 0's friends, which pairs among "
                "them already know each other, and the two formulas you ended up "
                "with. Crossings-out are fine and welcome.</span>"
        )
    mo.vstack([cp5_ring_paperwork_photo, _caption])
    return (cp5_ring_paperwork_photo,)


@app.cell(hide_code=True)
def cp5_ring_paperwork_photo_preview(cp5_ring_paperwork_photo, mo):
    from pathlib import Path as _P

    _files = list(cp5_ring_paperwork_photo.value or [])
    # A photo already saved means this session is over and someone is reading
    # the notebook. The drop box cannot remember the file across a restart, but
    # the saved copy is two cells below — so "your photo appears here once you
    # drop it in" was simply false to every later reader.
    _done = not _files and _P("assets/uploads/cp5_ring_paperwork_photo_view.jpg").exists()
    cp5_ring_paperwork_photo_send = mo.ui.run_button(label="📨 Send to my tutor", disabled=not _files)
    if _done:
        _out = None
    elif not _files:
        _out = mo.vstack([
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Your photo appears "
                "here once you drop it in above.*</span>"
            ),
            cp5_ring_paperwork_photo_send,
        ])
    else:
        _out = mo.vstack([
            mo.image(_files[0].contents, width=420),
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>This is exactly what "
                "your tutor will see. Want to fix a step and try again? Drop another "
                "photo into the box above — it replaces this one, as many times as "
                "you like. When it looks right, press send.</span>"
            ),
            cp5_ring_paperwork_photo_send,
        ])
    _out
    return (cp5_ring_paperwork_photo_send,)


@app.cell(hide_code=True)
def cp5_ring_paperwork_photo_sent(
    cp5_ring_paperwork_photo,
    cp5_ring_paperwork_photo_send,
    mo,
):
    from pathlib import Path as _P

    # Recomputed, not borrowed: a name starting with "_" is private to its cell
    # in marimo, so the preview cell's copy is not visible here.
    _done = not (cp5_ring_paperwork_photo.value or []) and _P("assets/uploads/cp5_ring_paperwork_photo_view.jpg").exists()
    if cp5_ring_paperwork_photo_send.value and (cp5_ring_paperwork_photo.value or []):

        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp5_ring_paperwork_photo\n")
        _sent = mo.md("✅ **Sent.** Your tutor is looking at it now.")
    else:
        _sent = (
            None
            if _done
            else mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Press the button above "
                "when the photo looks right — that is what tells your tutor to look.*</span>"
            )
        )
    _sent
    return


@app.cell(hide_code=True)
def cp5_ring_paperwork_photo_view(mo):
    from pathlib import Path as _P
    mo.vstack([
        mo.image(_P("assets/uploads/cp5_ring_paperwork_photo_view.jpg").read_bytes(), width=420),
        mo.md(r"""<span style='color:#6A6D75;font-size:13px'>📷 My own work on paper — the task: On a 12-dot ring with friend-count k, work through node 0s friends and clustering, reason that clustering depends only on k not N, work out hops across a 1000-person ring, and relate average path length L to N and k.</span>"""),
    ])
    return


@app.cell(hide_code=True)
def cp5_ring_formula_note(mo):
    mo.md(r"""
    ### 🔺 Clustering and path length on a ring — as formulas
    $N$ = people in the ring, $k$ = friends each person has ($k/2$ per
    side), $C$ = clustering (how often two of your friends know each
    other), $L$ = average distance (typical steps between two people).

    $$
    C(k) = \frac{3(k-2)}{4(k-1)}
    \qquad\qquad
    L(N,k) \approx \frac{N}{2k}
    $$

    Clustering is a function of $k$ ONLY, never $N$ ($k=2$ gives $C=0$,
    $k=4$ gives $C=0.5$). Every neighbourhood is identical, so counting
    around one node gives the whole ring. $L$ grows with the crowd
    instead: the farthest trip is about $N/k$ hops — half a ring at $k/2$
    places per hop — and the average is about half of that.
    """)
    return


@app.cell(hide_code=True)
def cp5_tension_note(mo):
    mo.md(r"""
    ### ⚖️ The puzzle: clustered AND close?
    Same four letters as before: $C$ = clustering (how often two of your
    friends know each other), $L$ = average distance (typical number of
    steps between two people), $N$ = how many people there are, $k$ = how
    many friends each person has.

    **Ring world:** tight communities (high $C$, independent of $N$) but
    journeys that get longer and longer as $N$ grows ($L \approx N/(2k)$).
    **Random world:** short journeys (low $L$) but no community (low
    $C$). This world has formulas too — throw everyone's $k$ friendships
    at random and both come out in closed form:

    $$
    C_{\text{random}} \approx \frac{k}{N}
    \qquad\qquad
    L_{\text{random}} \approx \frac{\log N}{\log k}
    $$

    Those two are clustering and average distance measured on the random
    world. The first is one hundredth when a thousand people have ten
    friends each. The second is just "how many times do I multiply by $k$
    before I have covered all $N$ people" — with ten friends each, 3 steps
    for a thousand people, 6 for a million, 9 for a billion.

    **Short paths are free.** Anything well mixed already has them, so the
    surprising half of six degrees was never the six — it is having six
    AND keeping the triangles. Real social networks somehow manage both,
    and neither extreme world explains it.
    """)
    return


@app.cell(hide_code=True)
def ch4_header(mo):
    mo.md(r"""
    ## Chapter 4 of 5 — Turning One Dial

    Chapter 3 ended in a tension. The ring world is clustered but far-flung; the random world is close but has no community. This chapter puts a dial between the two. Rewire a fraction $p$ of the ring's links to random targets. Then watch what each measure does as the dial turns: first on a slider, then with real code at N=2000.
    """)
    return


@app.cell(hide_code=True)
def cp6_legend(mo):
    mo.md(r"""
    **Reading the dials:** $p$ = the fraction of the ring's links picked
    up and reconnected to someone chosen at random. That is the slider below.
    $L$ = average distance, how many steps apart a typical pair is. $C$ =
    clustering, how often two of your friends know each other. $L_0$ and $C_0$
    are those same two numbers for the untouched ring ($p=0$). So $L/L_0 = 1$
    means "unchanged", and $L/L_0 = 0.2$ means distances shrank to a fifth.
    """)
    return


@app.cell(hide_code=True)
def cp6_p(mo):
    cp6_p = mo.ui.slider(
        steps=[0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0],
        value=0.0,
        label="rewiring probability p",
    )
    cp6_p
    return (cp6_p,)


@app.cell(hide_code=True)
def cp6_ws_fig(cp6_p, mo, netviz, nx):
    _p = float(cp6_p.value)
    _n, _k = 200, 4

    _ring = nx.watts_strogatz_graph(_n, _k, 0)
    _L0 = nx.average_shortest_path_length(_ring)
    _C0 = nx.average_clustering(_ring)

    _Ls, _Cs = [], []
    for _seed in (1, 2, 3):
        _H = nx.connected_watts_strogatz_graph(_n, _k, _p, seed=_seed) if _p > 0 else _ring
        _Ls.append(nx.average_shortest_path_length(_H))
        _Cs.append(nx.average_clustering(_H))
    _Lr = (sum(_Ls) / len(_Ls)) / _L0
    _Cr = (sum(_Cs) / len(_Cs)) / _C0

    import math as _math

    _D = nx.connected_watts_strogatz_graph(60, 4, _p, seed=5) if _p > 0 else nx.watts_strogatz_graph(60, 4, 0)
    _ringe = [e for e in _D.edges() if min(abs(e[0] - e[1]), 60 - abs(e[0] - e[1])) <= 2]
    _short = [e for e in _D.edges() if min(abs(e[0] - e[1]), 60 - abs(e[0] - e[1])) > 2]

    # Explicit node order (0..59) for the circle layout — netviz's "circle"
    # string layout orders nodes by first appearance in the edge list, and
    # nx.Graph.edges() after rewiring does NOT visit nodes in index order, so
    # the string layout scrambles node positions. Position every node ourselves.
    _pos60 = {
        _i: (
            0.5 + 0.42 * _math.cos(2 * _math.pi * _i / 60 - _math.pi / 2),
            0.5 + 0.42 * _math.sin(2 * _math.pi * _i / 60 - _math.pi / 2),
        )
        for _i in range(60)
    }
    mo.vstack([
        mo.md(
            f"**p = {_p} &nbsp;&nbsp; distance L/L₀ = {_Lr:.2f} &nbsp;&nbsp; "
            f"clustering C/C₀ = {_Cr:.2f}**\n\n"
            f"<span style='color:#6A6D75;font-size:13px'>The two numbers are measured "
            f"on a {_n}-person ring, averaged over 3 tries. The picture below is a "
            f"60-dot sketch of the same rewiring, small enough to see. **Grey lines "
            f"are the ring's original neighbour links.** **Rust lines are the ones "
            f"the slider has picked up and reconnected somewhere random.** Move the "
            f"slider one notch at a time and watch the two numbers above. Take one "
            f"number at a time: L/L₀ first, then C/C₀.</span>"
        ),
        netviz(_ringe + _short, highlight=_short, layout=_pos60, width=820, height=820),
    ])
    return


@app.cell(hide_code=True)
def cp6_rewire_step(mo):
    cp6_rewire_step = mo.ui.slider(
        start=0, stop=6, step=1, value=0, label="links rewired so far", show_value=True
    )
    cp6_rewire_step
    return (cp6_rewire_step,)


@app.cell(hide_code=True)
def cp6_rewire_fig(cp6_rewire_step, mo, netviz, nx):
    import math as _math
    import random as _random

    _N, _half, _STEPS, _SEED = 60, 2, 6, 29

    # The rewiring, replayed from the top every time so the picture at step s is
    # always the same picture — a slider the student drags back and forth must
    # not show them a different ring on the way back.
    _rng = _random.Random(_SEED)
    _edges = [tuple(sorted((_i, (_i + _d) % _N))) for _i in range(_N) for _d in range(1, _half + 1)]
    _lattice = set(_edges)
    _order = list(range(len(_edges)))
    _rng.shuffle(_order)
    _frames = [list(_edges)]
    _moved = 0
    for _idx in _order:
        if _moved == _STEPS:
            break
        _a, _b = _edges[_idx]
        _cand = [
            _c for _c in range(_N)
            if _c != _a and _c != _b and tuple(sorted((_a, _c))) not in _edges
        ]
        if not _cand:
            continue
        _edges[_idx] = tuple(sorted((_a, _rng.choice(_cand))))
        _moved += 1
        _frames.append(list(_edges))

    _s = int(cp6_rewire_step.value)
    _now = _frames[_s]
    _short = [_e for _e in _now if _e not in _lattice]
    _ring = [_e for _e in _now if _e in _lattice]

    # The newest cable's two ends, so the eye lands on what just changed.
    _newest = [_e for _e in _now if _e not in set(_frames[_s - 1])] if _s else []
    _ends = {_v for _e in _newest for _v in _e}

    _G = nx.Graph(_now)
    _L = nx.average_shortest_path_length(_G)
    _C = nx.average_clustering(_G)
    _G0 = nx.Graph(_frames[0])
    _L0 = nx.average_shortest_path_length(_G0)
    _C0 = nx.average_clustering(_G0)

    _pos = {
        _i: (
            0.5 + 0.42 * _math.cos(2 * _math.pi * _i / _N - _math.pi / 2),
            0.5 + 0.42 * _math.sin(2 * _math.pi * _i / _N - _math.pi / 2),
        )
        for _i in range(_N)
    }
    _colors = {_v: "#DAB167" for _v in _ends}

    mo.vstack([
        mo.md(
            f"**{_s} of the ring's {len(_now)} links moved &nbsp;&nbsp; "
            f"average distance L = {_L:.2f} &nbsp;&nbsp; clustering C = {_C:.2f}**\n\n"
            f"<span style='color:#6A6D75;font-size:13px'>Untouched, this ring has "
            f"L = {_L0:.2f} and C = {_C0:.2f}. **Grey lines are the ring's original "
            f"neighbour links.** **A rust line has been picked up and reconnected "
            f"to somebody chosen at random.** **The two amber dots are the ends of "
            f"the newest one.** Step the slider up one at a time and watch the two "
            f"numbers above. Drag any dot to see what its rust line reaches "
            f"across.</span>"
        ),
        netviz(
            _ring + _short,
            highlight=_short,
            node_colors=_colors,
            layout=_pos,
            width=820,
            height=820,
        ),
    ])
    return


@app.cell(hide_code=True)
def cp6_watts_strogatz_note(mo):
    mo.md(r"""
    ### 🎛️ The Watts–Strogatz recipe (1998)
    The dials: $p$ = the fraction of links picked up and reconnected to a
    random person; $L$ = average distance (typical steps between two
    people); $C$ = clustering (how often two of your friends know each
    other). $L_0$ and $C_0$ are the same two on the untouched ring, so the
    ratios read "compared to before".

    Rewiring about 1% of a ring's links already pulls distance down hard
    while clustering barely moves. On the 200-person ring in this slider:

    $$
    p \approx 0.01
    \qquad\Longrightarrow\qquad
    \frac{L}{L_0} \approx 0.6
    \qquad
    \frac{C}{C_0} \approx 1
    $$

    Those few rewires are the long cables from my
    drawing: rare enough to keep the communities, long enough to shortcut
    the ring. 200 people is a small ring, and the effect only sharpens
    with the crowd: the next cell runs the same sweep at $N = 2000$, where
    the same 1% takes distance far lower still. That's the small-world
    recipe, and it's why six degrees works.
    """)
    return


@app.cell(hide_code=True)
def cp6_large_n_ed(mo):
    cp6_large_n_ed = mo.ui.code_editor(value="# N is set for you — much bigger than the N=200 you played with.\nN = 2000\nk = 4\np_values = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]\n\nL0 = C0 = None\nrows = []\nfor p in p_values:\n    G = nx.connected_watts_strogatz_graph(N, k, p, seed=1) if p > 0 else nx.watts_strogatz_graph(N, k, 0)\n    # 1. Measure the average distance of G — nx.average_shortest_path_length\n    L = ...\n    # 2. Measure the average clustering of G — nx.average_clustering\n    C = ...\n    if p == 0.0:\n        L0, C0 = L, C\n    rows.append({\"p\": str(p), \"L/L0\": L / L0, \"C/C0\": C / C0})\n\ndf = pd.DataFrame(rows).melt(\"p\", var_name=\"measure\", value_name=\"ratio\")\nalt.Chart(df).mark_line(point=True).encode(\n    x=alt.X(\"p:O\", title=\"rewiring probability p\"),\n    y=alt.Y(\"ratio:Q\", title=\"ratio to p=0 baseline\"),\n    color=alt.Color(\n        \"measure:N\",\n        # Rust = L/L0, navy = C/C0. The domain MUST be bound: without\n        # it Vega sorts the categories and swaps the two colours.\n        scale=alt.Scale(domain=[\"L/L0\", \"C/C0\"], range=[\"#B14434\", \"#3959A6\"]),\n    ),\n).properties(title=f\"N={N}, k={k}\")", language="python", min_height=140)
    cp6_large_n_run = mo.ui.run_button(label="▶ Run my code")
    mo.vstack([mo.md(r"""Run the same sweep on a much bigger network — N = 2000 instead of 200. Fill in the two blanks (each function is named in the comment right above it), then press ▶ Run. Two lines, both measured against the untouched ring: **rust is L/L₀, the average distance; navy is C/C₀, the clustering.** Left to right is more rewiring."""), cp6_large_n_ed, cp6_large_n_run])
    return cp6_large_n_ed, cp6_large_n_run


@app.cell(hide_code=True)
def cp6_large_n_out(cp6_large_n_ed, cp6_large_n_run, mo, run_student_code):
    from pathlib import Path as _P
    _saved = _P("assets/exercises/cp6_large_n.py")
    cp6_large_n_send = mo.ui.run_button(
        label="📨 Send my code to my tutor",
        disabled=not (cp6_large_n_run.value or _saved.exists()),
    )
    if cp6_large_n_run.value:
        _saved.parent.mkdir(parents=True, exist_ok=True)
        _saved.write_text(cp6_large_n_ed.value)
        _res = mo.vstack([
            run_student_code(cp6_large_n_ed.value, {}),
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>Run it as many times "
                "as you like. When it does what you want, press 📨 — that is what "
                "hands it in and tells your tutor to look.</span>"
            ),
            cp6_large_n_send,
        ])
    elif _saved.exists():
        _res = mo.vstack([
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>The code I wrote and "
                "ran — press ▶ Run again after an edit to refresh this:</span>"
                "\n\n```python\n"
                + _saved.read_text()
                + "\n```"
            ),
            run_student_code(_saved.read_text(), {}),
            cp6_large_n_send,
        ])
    else:
        _res = mo.md("*Press ▶ Run when you're ready.*")
    _res
    return (cp6_large_n_send,)


@app.cell(hide_code=True)
def cp6_large_n_sent(cp6_large_n_send, mo):
    from pathlib import Path as _P
    if cp6_large_n_send.value:

        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp6_large_n_ed" + "\n")
        _sent = mo.md("✅ **Handed in.** Your tutor is reading your code now.")
    else:
        _sent = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*The 📨 button above is "
            "what hands this code to your tutor.*</span>"
            if _P("assets/exercises/cp6_large_n.py").exists()
            else "<span style='color:#6A6D75;font-size:13px'>*A 📨 hand-in button "
            "appears here once you have pressed ▶ Run.*</span>"
        )
    _sent
    return


@app.cell(hide_code=True)
def cp6_large_n_experiment_note(mo):
    mo.md(r"""
    ### 💻 The phase transition, at scale
    Same experiment as the slider, but coded and run on a much bigger
    network — $N$, the number of people, is 2000 here instead of 200. I
    swept $p$ (the fraction of links rewired at random) and plotted
    $L/L_0$ (average distance, compared to the untouched ring) against
    $C/C_0$ (clustering, compared to the untouched ring).
    """)
    return


@app.cell(hide_code=True)
def ch5_header(mo):
    mo.md(r"""
    ## Chapter 5 of 5 — Mastery Check

    No new machinery in this final chapter. Just two tests of whether the story holds. First, an AI hands me its analysis of a network. It asks me to sign off on it. Then a friend asks the question this module opened with, and I answer it in my own words.
    """)
    return


@app.cell(hide_code=True)
def cp7_claim(mo):
    mo.md(r"""
    ### 🤖 The analysis I was asked to sign off on

    > I analyzed your network. Its average clustering coefficient is
    > **0.61**, far higher than a random network's (**0.01**). Therefore
    > this is a small-world network.

    <span style='color:#6A6D75;font-size:13px'>Read it as the reviewer who
    has to sign underneath.</span>
    """)
    return


@app.cell(hide_code=True)
def cp7_redteam_note(mo):
    mo.md(r"""
    ### 🕵️ Reviewing an AI's claim
    "High clustering ⇒ small world" is NOT enough: small-world means BOTH
    high clustering AND short paths. My counterexample: the ring with
    nothing rewired ($p = 0$, where $p$ is the fraction of links picked
    up and reconnected at random) — very clustered, yet enormous
    distances. So both halves have to be measured: $C$ (clustering — how
    often two of your friends know each other) and $L$ (average distance —
    the typical number of steps between two people).

    Why not just divide one by the other? $C$ is never above 1 and $L$ is
    never below 1, so $C/L$ is biggest for the network where everyone
    already knows everyone ($C = 1$, $L = 1$) — the least interesting
    network there is. Raw numbers certify nothing. The **small-world
    index** compares both against a random network of the same size
    instead:

    $$
    \sigma = \frac{C / C_{\text{random}}}{L / L_{\text{random}}}
    \qquad\text{with}\qquad
    C_{\text{random}} \approx \frac{k}{N}
    \quad
    L_{\text{random}} \approx \frac{\log N}{\log k}
    $$

    — the two baselines from chapter 3, where $N$ is how many people
    there are and $k$ how many friends each one has.
    $\sigma > 1$ means small world: more clustered than random without
    paying for it in distance. $\sigma \approx 1$ means the network is
    indistinguishable from a random one.
    """)
    return


@app.cell(hide_code=True)
def cp8_wrapup_note(mo):
    mo.md(r"""
    ### 🎓 The whole story, in my own words
    Local links make clusters; a few long-range shortcuts exist; those
    shortcuts pull everyone close. That's how a letter crosses a country
    in about six steps.

    And not only a country of people. The same shape shows up wherever
    wiring is mostly local and expensive to stretch: a brain connects
    mostly to nearby neurons with a few long fibres crossing it, and the
    internet is mostly regional with a handful of cables spanning oceans.
    Both are small worlds for the same reason mine is.
    """)
    return


@app.cell(hide_code=True)
def session_record(mo):
    mo.md(r"""
    ## 📋 Session record

    *Your answer to each question, and every word you typed while working on*
    *it — this is what gets reviewed, not the code. Hints are never held*
    *against you.*

    **cp0_welcome** · pass

    *(no question — session greeting only)*

    > My initial guess is that the letter might need 6-8 people to reach the target.

    *You typed:* "My initial guess is that the letter might need 6-8 people to reach the target."

    *Tutor's note:* Session opened; student volunteered an early guess about the letter's hops before any question was asked.

    **cp1_milgram** · pass

    *For the packets that reached the Boston stockbroker, how many people handled one along the way, on average?*

    > It was very close to my guess. I guessed around 6-8 people, and the actual successful chains used about 5.2 intermediaries on average, so roughly six degrees of separation.

    *You chose:* "about 6"

    *You typed:* "It was very close to my guess. I guessed around 6-8 people, and the actual successful chains used about 5.2 intermediaries on average, so roughly six degrees of separation."

    *Tutor's note:* Guessed 6-8; picker chose "about 6"; reaction confirmed the real 5.2-average result matched his guess closely.

    **cp1_routing** · pass

    *If I told you, with total certainty, that SOME six-click path connects those two pages somewhere on Wikipedia — would that make the race easy to win? Why or why not?*

    > Not necessarily. Knowing that a six-click path exists tells me the two pages are close in the network, but it does not tell me which links form that path. At each page I still have many possible links to choose from, and most choices may lead away from the target. So the shortest path can be small even when finding that path using only local information is difficult.

    *You typed:* "Not necessarily. Knowing that a six-click path exists tells me the two pages are close in the network, but it does not tell me which links form that path. At each page I still have many possible links to choose from, and most choices may lead away from the target. So the shortest path can be small even when finding that path using only local information is difficult."

    *Tutor's note:* Articulated precisely that a short path existing differs from finding it with only local info — used Wikirace framing unprompted and correctly.

    **cp2_distance** · pass

    *What's the distance from A to D, and then the average over all 6 pairs?*

    > The distance from A to D is 2, because the shortest route uses two edges. Even though there are multiple possible routes, the shortest-path distance is the minimum number of edges, which is 2. There are 6 unordered pairs among 4 people. Five pairs are directly connected, so their distance is 1, while A–D has distance 2. Therefore the average shortest-path distance is 1+1+2+1+1+1/6 = approx 1.17. So on average, two people in this network are only about 1.17 steps apart.

    *You typed:* "The distance from A to D is 2, because the shortest route uses two edges. Even though there are multiple possible routes, the shortest-path distance is the minimum number of edges, which is 2." · "There are 6 unordered pairs among 4 people. Five pairs are directly connected, so their distance is 1, while A–D has distance 2. Therefore the average shortest-path distance is 1+1+2+1+1+1/6=approx 1.17 So on average, two people in this network are only about 1.17 steps apart."

    *Tutor's note:* Computed A-D=2 and average 7/6≈1.17 on first try, with clear reasoning about shortest vs any route and the pair count.

    **cp2_diameter** · pass

    *Which pair is the single longest trip in this network, and how many edges?*

    > The pair is A-D, with distance 2. Every other pair is directly connected with distance 1, so A-D is the longest shortest path in the network. Therefore the network’s diameter is 2.

    *You typed:* "The pair is A-D, with distance 2. Every other pair is directly connected with distance 1, so A-D is the longest shortest path in the network. Therefore the network’s diameter is 2."

    *Tutor's note:* Named A-D at 2 and even supplied the term "diameter" himself before it was introduced.

    **cp2_paperwork** · pass

    *By hand, find the distance for all 10 pairs on the 5-ring, then the average.*

    > I drew a 5-node ring with nodes A, B, C, D, and E, connected only to their two neighbors: A–B, B–C, C–D, D–E, and E–A. The pairwise distances I got are: A–B = 1, A–C = 2, A–D = 2, A–E = 1, B–C = 1, B–D = 2, B–E = 2, C–D = 1, C–E = 2, and D–E = 1. The total distance is 15 across 10 pairs, so the average path length is 15/10 = 1.5

    *You typed:* "I drew a 5-node ring with nodes A, B, C, D, and E, connected only to their two neighbors: A–B, B–C, C–D, D–E, and E–A. The pairwise distances I got are: A–B = 1, A–C = 2, A–D = 2, A–E = 1, B–C = 1, B–D = 2, B–E = 2, C–D = 1, C–E = 2, and D–E = 1. The total distance is 15 across 10 pairs, so the average path length is 15/10 = 1.5"

    *Tutor's note:* Photo was uploaded but could not be read on the tutor's side (whiteboard image view unavailable), so student typed the full table: all 10 pair distances correct, average 15/10 = 1.5. Hand-worked page was still produced and submitted.

    **cp3_clustering** · pass

    *How many friendships actually exist among A's 5 friends, and what fraction is that?*

    > There are 2 actual friendships among Alice’s five friends. Since 10 friendships are possible, Alice’s local clustering is  2/10=0.2.

    *You typed:* "Alice has the same number of friends in both cases, so her degree is the same. What changes is the amount of connection among her five friends. In the first case, none of Alice’s friends know each other, so there are no links among her neighbors. In the second case, every one of her friends knows every other friend, so her neighborhood is fully connected. This is capturing local clustering: how tightly connected a node’s neighbors are to each other." · "I would count how many connections exist between Alice’s friends and compare that with how many connections could possibly exist between them. If none of her friends know each other, the value is 0. If all of them know each other, the value is 1." · "There are 2 actual friendships among Alice’s five friends. Since 10 friendships are possible, Alice’s local clustering is  2/10=0.2."

    *Tutor's note:* Identified the difference as lines between friends and named clustering; counted 2 of 10 actual friendships and computed 0.2 correctly in one breath.

    **cp3_average** · pass

    *B's score, then C/E/F's scores, then D's (with one friend), then average all six.*

    > B knows A and F. Those two are also connected, so B's score is 1.0. C, E, and F all have the same score as B: 1.0, because in each case their two friends are also connected. D has only one friend, so there is no pair of D's friends that could be connected — zero possible links to evaluate. The average local clustering coefficient is 0.7.

    *You typed:* "B knows A and F. Those two are also connected to each other, so B’s two neighbors form the only possible connection between them. So B’s local clustering score is 1.0 or 100%" · "C, E, and F all have the same score as B: 1.0, because in each case their two friends are also connected to each other." · "D has only one friend, so there is no pair of D’s friends that could be connected. There are zero possible friend-to-friend links to evaluate." · "The average local clustering coefficient is 0.7. I added the six individual scores and divided by six."

    *Tutor's note:* Scored B, C, E, F = 1 each, recognized D has zero pairs to check (hence 0 by convention), and averaged to 0.70 correctly.

    **cp3_global_clustering** · pass

    *Why does the global measure land near Alice's 0.2 while the average said 0.70?*

    > The global measure gives more weight to people who center many triplets. Alice alone accounts for 10 of the 14 triplets, and her neighborhood is only weakly clustered, so her low value has a much bigger influence. In the average local clustering, every person counts equally, which is why that value was much higher at 0.70.

    *You typed:* "A closed triplet" · "There are 2 triangles in the whole network. A–B–F and A–C–E. Each of those trios has all three connections present." · "B, C, E, and F each center 1 triplet, D centers 0, and Alice centers 10, so the network has 14 triplets altogether." · "The network’s global clustering coefficient is about 0.43. That is lower than the average local clustering of 0.70, so the two ways of measuring clustering do not have to agree." · "The global measure gives more weight to people who center many triplets. Alice alone accounts for 10 of the 14 triplets, and her neighborhood is only weakly clustered, so her low value has a much bigger influence. In the average local clustering, every person counts equally, which is why that value was much higher at 0.70."

    *Tutor's note:* Named closed triplet, found 2 triangles, totaled 14 triplets (10+1+1+1+1+0), computed 0.43, and — unprompted and precisely — explained the hub-weighting reason for the 0.70 vs 0.43 gap.

    **cp4_shortcut_drawing** · pass

    *On 8 dots the gap is small. What would you expect on a ring of 800?*

    > On a ring of 800 nodes, I would expect the long cable to make a much bigger difference. Without shortcuts, many pairs of nodes are very far apart because you have to travel around the ring step by step. A long-range cable connects distant parts of the network directly, so it can shorten the routes for many different pairs at once. As the ring gets larger, that kind of shortcut should become much more valuable than a short cable between already-nearby nodes.

    *You typed:* "I connected A and E, the two dots directly opposite each other on the 8-node ring. I chose them because they were originally 4 steps apart, so I expected that shortcut to reduce many shortest-path distances across the network." · "On a ring of 800 nodes, I would expect the long cable to make a much bigger difference. Without shortcuts, many pairs of nodes are very far apart because you have to travel around the ring step by step. A long-range cable connects distant parts of the network directly, so it can shorten the routes for many different pairs at once. As the ring gets larger, that kind of shortcut should become much more valuable than a short cable between already-nearby nodes."

    *Tutor's note:* Connected A–E straight across (the long-range choice) with sound reasoning; then predicted the gap widens on a bigger ring, correctly seeing long cables save many steps at once.

    **cp5_ring_formula** · pass

    *Does clustering depend on N, and how does L relate to N and k?*

    > No, clustering depends on k not N. L grows with N and shrinks with k, roughly N/(2k).

    *You typed:* "No, it shows 3 connected pairs, not 2. I missed the connection between 11 and 1 across node 0’s neighborhood. So for K=4, node 0 has 4 friends and 3 actual links among those friends." · "Node 0’s clustering coefficient is 3/6 = 0.5, because 3 of the 6 possible friendships among its four friends actually exist." · "No. For this regular k=4 ring, node 0 still has the same four friends, and the same 3 of 6 possible connections among those friends are present. So its clustering stays 3/6=0.5. In this setup, the local clustering depends on k, not on the total number of people N." · "It would take about 250 hops to reach the person directly opposite me. That shows that, unlike clustering, path length grows with the size N of the ring." · "The average path length L grows as N grows, because a larger ring means people are spread farther apart. It shrinks as K grows, because having more friends lets each hop cover more of the ring. So, roughly, L increases with N and decreases with K."

    *Tutor's note:* Worked k=2 (no triangles) and k=4 (caught the missed 11-1 pair via the count box, 3/6=0.5), stated C depends only on k not N, got 250 hops for N=1000/k=4, and wrote L≈N/(2k). Even generalized C(k)=3(k-2)/(4(k-1)) on his own page. Photo read successfully this time.

    **cp5_tension** · pass

    *Ring world and random world — what do your C and L formulas say about each, and which world do you live in?*

    > I think the real world is a mix of the two. My friends often know each other, so clustering is high, but I also have some connections to people far outside my local group, which create shortcuts. So real social networks can have both high clustering and short average path lengths.

    *You typed:* "Yes. If everyone still knows only their nearest few neighbors on the ring, the people around me will still tend to know each other. The clustering coefficient stays determined by k, not by the total population size. So making the country much larger does not by itself reduce local clustering." · "It would take a very long time compared with a small network. Since L grows with N, making the ring country-sized makes typical routes huge unless K also grows. So the network can have high clustering but still have very long paths." · "L becomes small, because random long-range connections create shortcuts across the country, so you can reach distant people in relatively few steps. C becomes low, because your friends are scattered randomly and are therefore unlikely to also know each other." · "I think the real world is a mix of the two. My friends often know each other, so clustering is high, but I also have some connections to people far outside my local group, which create shortcuts. So real social networks can have both high clustering and short average path lengths."

    *Tutor's note:* Correctly read both worlds off his own formulas — ring: high C, L grows; random: L small, C low — and concluded the real world is a mix with both, precisely the instinct the next chapter builds on.

    **cp6_watts_strogatz** · pass

    *Which single notch drops L/L0 the most, and what is C/C0 at that notch?*

    > The biggest single-notch drop in normalized distance happens at \(p=0.05\), where L/L0 falls from 0.61 to 0.29, a drop of 0.32. At the same point, C/C0=0.84, which is still close to 1. So only a small amount of rewiring greatly shortens paths while preserving most of the original clustering.

    *You chose:* "distance drops a lot, clustering barely changes"

    *You typed:* "The biggest single-notch drop in normalized distance happens at \(p=0.05\), where L/L0 falls from 0.61 to 0.29, a drop of 0.32. At the same point, C/C0=0.84, which is still close to 1. So only a small amount of rewiring greatly shortens paths while preserving most of the original clustering."

    *Tutor's note:* Prediction correct upfront; then read the steepest drop at p=0.05 (0.61→0.29, drop 0.32) with C/C0=0.84 still high, and reconciled it to the formulas unprompted.

    **cp6_large_n_experiment** · pass

    *At which p does L/L0 drop steepest, what is C/C0 there, and is that p smaller than on the 200-person ring?*

    > The steepest drop in L/L0 happens at about p=0.001, where the normalized distance falls from 1.00 to roughly 0.52. At that same point, C/C0 is still almost 1. Compared with the 200-person ring, this happens at a smaller rewiring probability, so the small-world effect appears even earlier in the larger network.

    *You typed:* "The steepest drop in L/L0 happens at about p=0.001, where the normalized distance falls from 1.00 to roughly 0.52. At that same point, C/C0 is still almost 1. Compared with the 200-person ring, this happens at a smaller rewiring probability, so the small-world effect appears even earlier in the larger network."

    *Tutor's note:* Filled both blanks correctly, ran clean, and read the steepest drop at p=0.001 with C/C0≈1, correctly naming it smaller than the N=200 notch — the graded half.

    **cp7_redteam** · pass

    *An AI claims small-world from clustering 0.61 vs 0.01 alone. You're the reviewer who has to sign off. Do you?*

    > \I would not approve that conclusion yet. High clustering compared with a random network is only one half of the small-world property. We also need to check whether the network’s average path length is close to the random network’s path length. A small-world network should have both high clustering and short paths, so the assistant’s evidence is incomplete.

    *You typed:* "\I would not approve that conclusion yet. High clustering compared with a random network is only one half of the small-world property. We also need to check whether the network’s average path length is close to the random network’s path length. A small-world network should have both high clustering and short paths, so the assistant’s evidence is incomplete."

    *Tutor's note:* Refused to sign off, correctly naming that path length was never measured and that small-world needs both high clustering AND short paths — even gestured at the random-baseline comparison (the bonus).

    **cp8_wrapup** · pass

    *How can a letter cross a whole country in about six steps?*

    > A country can still feel “small” because most people belong to close local groups, but a few connections reach far outside those groups. Those long-distance connections act like shortcuts, so a message can jump across large parts of the network very quickly. That is why two people who seem very far apart can still be connected through only a few other people.

    *You typed:* "A country can still feel “small” because most people belong to close local groups, but a few connections reach far outside those groups. Those long-distance connections act like shortcuts, so a message can jump across large parts of the network very quickly. That is why two people who seem very far apart can still be connected through only a few other people."

    *Tutor's note:* Explained the phenomenon end to end in plain words, hitting all three beats — local clusters, a few long-range shortcuts, shortcuts pulling everyone close — with no jargon and no hints.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    tutor_stuck_text = mo.ui.text_area(
        placeholder=(
            "What's going on? e.g. \"I answered this and I think it should count\", "
            "\"I'd like a fresh try at this one\", \"we're going in circles — let's move on\""
        ),
        rows=2,
    )
    tutor_stuck_send = mo.ui.run_button(label="⚖️ Tutor gets stuck — call the referee")
    # NOT an accordion. This is the student's only way out from under a tutor
    # that has stopped helping, and behind a closed accordion at the foot of a
    # long page it is something they have to already know about to find. It is
    # pinned below the newest material precisely so it is in view; it has to be
    # legible there without a click. Small and grey, so it reads as furniture
    # rather than competing with the lesson.
    mo.vstack([
        mo.md("<hr style='border:none;border-top:1px solid #E4E6EA;margin:18px 0 6px'>"),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>⚖️ <strong>Stuck with your "
            "tutor?</strong> If the two of you are going in circles — you think an "
            "answer should count, you want a fresh try, or you'd rather move on — "
            "say so here and press the button. A second, stronger model reads the "
            "whole situation and makes a call your tutor has to follow. Using it is "
            "never held against you.</span>"
        ),
        tutor_stuck_text,
        tutor_stuck_send,
    ])
    return tutor_stuck_send, tutor_stuck_text


@app.cell(hide_code=True)
def _(mo, tutor_stuck_send, tutor_stuck_text):
    from pathlib import Path as _P_appeal

    if tutor_stuck_send.value:
        _P_appeal("session_artifacts").mkdir(exist_ok=True)
        (_P_appeal("session_artifacts") / "appeal.txt").write_text(
            (tutor_stuck_text.value or "").strip() or "(no details given)"
        )
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("tutor_stuck\n")
        _appeal_out = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>✅ <strong>The referee is "
            "reading your case.</strong> It can take a minute — your tutor will "
            "come back to you in the terminal with the decision.</span>"
        )
    else:
        _appeal_out = mo.md("")
    _appeal_out
    return


if __name__ == "__main__":
    app.run()
