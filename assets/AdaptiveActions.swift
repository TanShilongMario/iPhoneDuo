import SwiftUI

/// Attach to content inside a NavigationStack/NavigationSplitView.
/// The system chooses the bar edge and overflow; no camera offsets or device checks.
/// The caller keeps its existing implementation on systems earlier than iOS 27.1.
@available(iOS 27.1, *)
struct AdaptiveActions<Overflow: View>: ViewModifier {
    let primaryTitle: LocalizedStringKey
    let primarySymbol: String
    let primaryAction: () -> Void
    let secondaryTitle: LocalizedStringKey
    let secondarySymbol: String
    let secondaryAction: () -> Void
    @ViewBuilder var overflow: () -> Overflow

    func body(content: Content) -> some View {
        content.toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                Button(primaryTitle, systemImage: primarySymbol, action: primaryAction)
            }
            .axisBehavior(.verticalPreferred)
            .visibilityPriority(.high)

            ToolbarItem(placement: .topBarTrailing) {
                Button(secondaryTitle, systemImage: secondarySymbol, action: secondaryAction)
            }
            .axisBehavior(.verticalPreferred)

            ToolbarOverflowMenu { overflow() }
        }
    }
}
