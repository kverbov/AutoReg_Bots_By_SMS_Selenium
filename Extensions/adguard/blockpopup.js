/**
 * This file is part of Adguard Browser Extension (https://github.com/AdguardTeam/AdguardBrowserExtension).
 *
 * Adguard Browser Extension is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Adguard Browser Extension is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with Adguard Browser Extension.  If not, see <http://www.gnu.org/licenses/>.
 */

(function (adguard) {
    'use strict';

    const tabsLoading = Object.create(null);

    function checkPopupBlockedRule(tabId, requestUrl, referrerUrl, sourceTab) {
        // Tab isn't ready
        if (!requestUrl) {
            return;
        }

        delete tabsLoading[tabId];

        const requestRule = adguard.webRequestService.getRuleForRequest(
            sourceTab,
            requestUrl,
            referrerUrl,
            adguard.RequestTypes.DOCUMENT
        );

        if (adguard.webRequestService.isPopupBlockedByRule(requestRule)) {
            // remove popup tab
            adguard.tabs.remove(tabId);
            adguard.webRequestService.postProcessRequest(
                sourceTab,
                requestUrl,
                referrerUrl,
                adguard.RequestTypes.DOCUMENT,
                requestRule
            );
            adguard.requestContextStorage.recordEmulated(
                requestUrl,
                referrerUrl,
                adguard.RequestTypes.DOCUMENT,
                sourceTab,
                requestRule
            );
        }
    }

    adguard.webNavigation.onCreatedNavigationTarget.addListener((details) => {
        const sourceTab = { tabId: details.sourceTabId };

        // Don't process this request
        if (adguard.frames.isTabAdguardDetected(sourceTab)) {
            return;
        }

        // webRequest.onBeforeRequest event may hasn't been received yet.
        const referrerUrl = adguard.frames.getMainFrameUrl(sourceTab) || details.url;
        if (!adguard.utils.url.isHttpRequest(referrerUrl)) {
            return;
        }

        const { tabId } = details;
        tabsLoading[tabId] = {
            referrerUrl,
            sourceTab,
        };

        checkPopupBlockedRule(tabId, details.url, referrerUrl, sourceTab);
    });

    adguard.tabs.onUpdated.addListener((tab) => {
        const { tabId } = tab;

        if (!(tabId in tabsLoading)) {
            return;
        }

        if (tab.url) {
            const tabInfo = tabsLoading[tabId];
            if (tabInfo) {
                checkPopupBlockedRule(tabId, tab.url, tabInfo.referrerUrl, tabInfo.sourceTab);
            }
        }
    });
})(adguard);
